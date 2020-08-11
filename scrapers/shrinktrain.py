cntr = 0
with open('../data/css10/train.txt', 'r', encoding='utf-8') as f:
    with open('../data/css10/newtrain.txt', 'w', encoding='utf-8') as f2:
        for line in f:
            if cntr % 4 != 3:
                print(line.rstrip(), file=f2)
            cntr += 1

