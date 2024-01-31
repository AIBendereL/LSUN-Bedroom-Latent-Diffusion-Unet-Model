# AUTOGENERATED! DO NOT EDIT! File to edit: ../image_generator_norm_layernorm_layernorm_sampling.ipynb.

# %% auto 0
__all__ = ['device', 'SamplesEval']

# %% ../image_generator_norm_layernorm_layernorm_sampling.ipynb 120
import torch

from itertools import islice

import fastcore.all as fc
from fastprogress import progress_bar

from torchmetrics.image.fid import FrechetInceptionDistance
from torchmetrics.image.kid import KernelInceptionDistance

# %% ../image_generator_norm_layernorm_layernorm_sampling.ipynb 121
device = "cuda" if torch.cuda.is_available() else "cpu"
device

# %% ../image_generator_norm_layernorm_layernorm_sampling.ipynb 122
class SamplesEval():

    def __init__(self, dls_eval, percent= 1., device= device): 

        fc.store_attr()
        self.n_batch = int(len(dls_eval) * percent)

    # ------------------------------

    def progress_bar_sub_dls(self):

        sub_dls = islice(self.dls_eval, self.n_batch)
        return zip(progress_bar(range(self.n_batch)), sub_dls)

    # ------------------------------
        
    def init_fid(self, feature= 2048, reset_real_features= False, **kwargs):

        self.fid = FrechetInceptionDistance(feature= feature, 
                                            reset_real_features= reset_real_features, 
                                            **kwargs).to(self.device)
        
        for i, (imgs, lbls) in self.progress_bar_sub_dls(): self.fid.update(imgs.type(torch.uint8).to(self.device), 
                                                                            real= True)

    def fid_update(self, samples): self.fid.update(samples.type(torch.uint8).to(self.device), real= False)
    def fid_compute(self): return self.fid.compute()
    def fid_reset(self): self.fid.reset()
        
    def fid_eval(self, samples):

        self.fid_update(samples)
        result = self.fid_compute()
        self.fid_reset()
        
        return result
    
    # ------------------------------
    
    def init_kid(self, feature= 2048, subset_size= 32, reset_real_features= False, **kwargs):

        self.kid = KernelInceptionDistance(feature= feature, 
                                           subset_size= subset_size, 
                                           reset_real_features= reset_real_features,
                                           **kwargs).to(self.device)

        for i, (imgs, lbls) in self.progress_bar_sub_dls(): self.kid.update(imgs.type(torch.uint8).to(self.device), 
                                                                            real= True)

    def kid_update(self, samples): self.kid.update(samples.type(torch.uint8).to(self.device), real= False)
    def kid_compute(self): return self.kid.compute()
    def kid_reset(self): self.kid.reset()

    def kid_eval(self, samples):

        self.kid_update(samples)
        result = self.kid_compute()
        self.kid_reset()

        return result
