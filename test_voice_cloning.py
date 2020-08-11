import sys
import os
#import IPython
#from IPython.display import Audio


inputs = [
  #"Tā zhù zài gōngyuán pángbiān de jiē shàng|00-zh|zh",
   "wǒ xiànzài bù dǎsuàn cānjiā hěnduō xuǎnjǔ yīnwèi wǒ bù bì zàicì jìng xuǎn gōng zhí |02-zh|zh",
   # "Hello I am speaking very good words|00-zh|en",
  #"|02-zh|fr" #No me gusta comer en un lugar con mucha gente.
]
#inputs = [
     #"The fact that I am speaking english does not mean anything to me|02-en|en"
    #"Ese fuego por dentro me está enloqueciendo, me va saturando|00-en|es",
     #"Quiero respirar tu cuello despacito|00-en|es",
    # "Quiero respirar tu cuello despacito|00-sp|sp",
     # "But what I appreciate the most is that you have never.|00-fr|en",
     #"Quiero respirar tu cuello despacito.|00-zh|es"
    #"wǒ de zhōngwén hěn zāogāo dànshì wǒ yào xué zhōngwén|25-zh|zh",
    #"One two three four.|00-zh|en",
  #"The right of citizens of the United States, who are eighteen years of age or older, to vote shall not be denied.|00-en|en"
     # "Ese fuego por dentro me está enloqueciendo, me va saturando|00-es|es",
    #"The bars at the end of the street are quite loud and unfriendly.|00-en|en",
#"The bars at the end of the street are quite loud and unfriendly.|05-en|en",
#"The bars at the end of the street are quite loud and unfriendly.|00-es|en",
#"I used to be president of the united states|00-es|en",
#"The bars at the end of the street are quite loud and unfriendly.|00-zh|en",
#"The bars at the end of the street are quite loud and unfriendly.|02-zh|en",
     # "wǒ de zhōngwén hěn zāogāo dànshì wǒ yào xué zhōngwén|25-zh|zh",
  #  "Ese fuego por dentro me está enloqueciendo, me va saturando|00-en|es",
   #  "Ese fuego por dentro me está enloqueciendo, me va saturando|00-zh|es",
   #  "Ese fuego por dentro me está enloqueciendo, me va saturando|00-en|es"
#"wǒ de zhōngwén hěn zāogāo dànshì wǒ yào xué zhōngwén|25-zh|zh"
#]




#inputs = [
    # "There is a time and place for everything|english|english",
    # "There is a time and place for everything|french|english",
    # "There is a time and place for everything|chinese|english",
    # "Wǒ xǐhuān pǎo lái pǎo qù chīfàn|chinese|chinese",
    # "Wǒ xǐhuān pǎo lái pǎo qù chīfàn|french|chinese",
    # "Wǒ xǐhuān pǎo lái pǎo qù chīfàn|english|chinese"
#]

tacotron_dir = "Multilingual_Text_to_Speech"
wavernn_dir = "WaveRNN"
tacotron_chpt = "GENERATED-SWITCHING_loss-194-0.139"
wavernn_chpt = "wavernn_weight.pyt"



if "utils" in sys.modules:
    del sys.modules["utils"]

from synthesize import synthesize
from utils import build_model
model = build_model(os.path.join(os.path.join(os.getcwd(), "checkpoints"), tacotron_chpt))
model.eval()


spectrograms = [synthesize(model, "|" + i) for i in inputs]
#print(spectrograms[0].shape)

os.chdir(os.path.join(os.path.join(os.path.dirname(os.getcwd()), wavernn_dir)))
if "utils" in sys.modules:
    del sys.modules["utils"]

print(os.getcwd())

sys.path.insert(0, os.getcwd())
from models.fatchord_version import WaveRNN
from utils import hparams as hp
from gen_wavernn import generate
import torch

hp.configure('hparams.py')
model = WaveRNN(rnn_dims=hp.voc_rnn_dims, fc_dims=hp.voc_fc_dims, bits=hp.bits, pad=hp.voc_pad, upsample_factors=hp.voc_upsample_factors,
                feat_dims=hp.num_mels, compute_dims=hp.voc_compute_dims, res_out_dims=hp.voc_res_out_dims, res_blocks=hp.voc_res_blocks,
                hop_length=hp.hop_length, sample_rate=hp.sample_rate, mode=hp.voc_mode).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))

model.load(os.path.join(os.path.join(os.path.dirname(os.getcwd()), "checkpoints"), wavernn_chpt))

waveforms = [generate(model, s, hp.voc_gen_batched, hp.voc_target, hp.voc_overlap) for s in spectrograms]

from scipy.io.wavfile import write
import numpy as np

os.chdir(os.path.join(os.path.join(os.path.dirname(os.getcwd()), "audiofiles")))
for idx, w in enumerate(waveforms):
  print(inputs[idx])
  print(w)
  w_scaled = np.int16(w/np.max(np.abs(w)) * 32767)
  write('test' + str(idx+2) + '_194.wav', hp.sample_rate, w_scaled)
  #IPython.display.display(IPython.display.Audio(data=w, rate=hp.sample_rate))