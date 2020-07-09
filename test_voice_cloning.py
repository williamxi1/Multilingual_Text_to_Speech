import sys
import os
#import IPython
#from IPython.display import Audio


inputs = [
    "Wǒ xiǎng měitiān chī ròu, dàn wǒ shì sùshí zhǔyì zhě|02-zh|zh",
]
tacotron_dir = "Multilingual_Text_to_Speech"
wavernn_dir = "WaveRNN"
tacotron_chpt = "generated_switching.pyt"
wavernn_chpt = "wavernn_weight.pyt"



if "utils" in sys.modules:
    del sys.modules["utils"]

from synthesize import synthesize
from utils import build_model
os.chdir(os.path.join(os.path.expanduser("~"), tacotron_dir))
model = build_model(os.path.join(os.path.expanduser("~"), "checkpoints", tacotron_chpt))
model.eval()

spectrograms = [synthesize(model, "|" + i) for i in inputs]
#print(spectrograms[0].shape)

os.chdir(os.path.join(os.path.expanduser("~"), wavernn_dir))
if "utils" in sys.modules:
    del sys.modules["utils"]

print(os.getcwd())

sys.path.insert(0, os.path.join(os.path.expanduser("~"), wavernn_dir))
from models.fatchord_version import WaveRNN
from utils import hparams as hp
from gen_wavernn import generate
import torch

hp.configure('hparams.py')
model = WaveRNN(rnn_dims=hp.voc_rnn_dims, fc_dims=hp.voc_fc_dims, bits=hp.bits, pad=hp.voc_pad, upsample_factors=hp.voc_upsample_factors,
                feat_dims=hp.num_mels, compute_dims=hp.voc_compute_dims, res_out_dims=hp.voc_res_out_dims, res_blocks=hp.voc_res_blocks,
                hop_length=hp.hop_length, sample_rate=hp.sample_rate, mode=hp.voc_mode).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
model.load(os.path.join(os.path.expanduser("~"), "checkpoints", wavernn_chpt))

waveforms = [generate(model, s, hp.voc_gen_batched, hp.voc_target, hp.voc_overlap) for s in spectrograms]

from scipy.io.wavfile import write
import numpy as np

os.chdir(os.path.join(os.path.expanduser("~"), "audiofiles"))
for idx, w in enumerate(waveforms):
  print(inputs[idx])
  print(w)
  w_scaled = np.int16(w/np.max(np.abs(w)) * 32767)
  write('test.wav', hp.sample_rate, w_scaled)
  #IPython.display.display(IPython.display.Audio(data=w, rate=hp.sample_rate))