# -*- coding: utf-8 -*-
from .__module__ import Module, dependency, source, version
from .tools import Tools
from .python import Python
from .kaldi import Kaldi

@dependency(Kaldi, Python)
@source('git')
class Pykaldi(Module):
    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                graphviz \
			    libatlas3-base \
			    pkg-config \
                && \
            
            $PIP_INSTALL \
                pyparsing \
                ninja \
                && \

            $GIT_CLONE https://github.com/pykaldi/pykaldi.git ~/pykaldi --recursive && \
            cd ~/pykaldi/tools && \
            ./check_dependencies.sh && \
            ./install_protobuf.sh && \
            ./install_clif.sh && \
            ./install_kaldi.sh && \
            cd .. && \
            python setup.py install && \
        '''