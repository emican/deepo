# -*- coding: utf-8 -*-
# based on https://github.com/kaldi-asr/kaldi/tree/master/docker
from .__module__ import Module, dependency, source, version
from .tools import Tools
from .python import Python


@dependency(Tools)
@source('git')
class Kaldi(Module):

    def build(self):
        return r'''
            DEBIAN_FRONTEND=noninteractive $APT_INSTALL \
                sudo \
                g++ \
                make \
                automake \
                autoconf \
                bzip2 \
                sox \
                libtool \
                subversion \
                python2.7 \
                python3 \
                zlib1g-dev \
                patch \
                ffmpeg \
                gfortran \
            && \
            ln -s /usr/bin/python2.7 /usr/bin/python \
            && \
            $GIT_CLONE https://github.com/kaldi-asr/kaldi.git /opt/kaldi --recursive && \
            cd /opt/kaldi/tools && \
            ./extras/install_mkl.sh && \
            make -j $(nproc) && \
            cd /opt/kaldi/src && \
            ./configure --shared ''' + ([r'''--use-cuda && \ ''',r'''&& \ '''][self.composer.cuda_ver is None]
            ) + r'''
            find /opt/kaldi  -type f \( -name "*.o" -o -name "*.la" -o -name "*.a" \) -exec rm {} \; && \
            find /opt/intel -type f -name "*.a" -exec rm {} \; && \
            find /opt/intel -type f -regex '.*\(_mc.?\|_mic\|_thread\|_ilp64\)\.so' -exec rm {} \; && \
            rm -rf /opt/kaldi/.gi && \
        '''