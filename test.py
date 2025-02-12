import torch
import torch.nn.functional as F
from torch.autograd import Variable
from dataset import MyTestData
from model import Deconv
import densenet
import numpy as np
import os
import sys
import argparse
import time
from PIL import Image




home = os.path.expanduser("~")

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default='input')  # test dataset
parser.add_argument('--output_dir', default='mask')  # test dataset
parser.add_argument('--para_dir', default='parameters')  # parameters
parser.add_argument('--b', type=int, default=1)  # batch size
parser.add_argument('--q', default='densenet121')  # save checkpoint parameters
opt = parser.parse_args()
print(opt)



def main():
    if not os.path.exists(opt.output_dir):
        os.mkdir(opt.output_dir)
    bsize = opt.b

    feature = getattr(densenet, opt.q)(pretrained=False)
    feature.cpu()
    feature.eval()
    sb = torch.load(os.path.join('parameters_densenet121', 'feature_model.pth'), map_location=torch.device('cpu'))

    feature.load_state_dict(sb)

    deconv = Deconv(opt.q)
    deconv.cpu()
    deconv.eval()
    sb = torch.load(os.path.join('parameters_densenet121', 'deconv_model.pth'), map_location=torch.device('cpu'))


    deconv.load_state_dict(sb)
    test_loader = torch.utils.data.DataLoader(MyTestData(opt.input_dir), batch_size=bsize, shuffle=False, num_workers=1, pin_memory=False)

    step_len = len(test_loader)
    for id, (data, img_name, img_size) in enumerate(test_loader):
        inputs = Variable(data).cpu()
        start_time = time.time()
        feats = feature(inputs)
        outputs = deconv(feats)
        outputs = F.sigmoid(outputs)
        outputs = outputs.data.cpu().squeeze(1).numpy()
        end_time = time.time()

        for i, msk in enumerate(outputs):
            msk = (msk * 255).astype(np.uint8)
            msk = Image.fromarray(msk)
            msk = msk.resize((img_size[0][i], img_size[1][i]))
            msk.save(os.path.join(opt.output_dir, '%s.png' % img_name[i]), 'PNG') 

        # 显示进度
        step_now = id + 1
        step_schedule_num = int(40 * step_now / step_len)
        print("\r", end="")
        print("step: {}/{} [{}{}] - time: {:.2f}ms".format(step_now, step_len,
                                                           ">" * step_schedule_num,
                                                           "-" * (40 - step_schedule_num),
                                                           (end_time - start_time) * 1000), end="")
        sys.stdout.flush()

    print("\r")


if __name__ == "__main__":
    main()
