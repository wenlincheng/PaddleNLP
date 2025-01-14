# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections
import os

from paddle.dataset.common import md5file
from paddle.utils.download import get_path_from_url

from paddlenlp.utils.env import DATA_HOME

from . import DatasetBuilder

__all__ = ["PTB"]


class PTB(DatasetBuilder):
    """
    This is the Penn Treebank Project: Release 2 CDROM, featuring a million
    words of 1989 Wall Street Journal material.
    """

    URL = "https://bj.bcebos.com/paddlenlp/datasets/rnnlm/simple-examples.tgz"
    MD5 = "30177ea32e27c525793142b6bf2c8e2d"
    META_INFO = collections.namedtuple("META_INFO", ("file", "md5"))
    SPLITS = {
        "train": META_INFO(
            os.path.join("simple-examples", "data", "ptb.train.txt"), "f26c4b92c5fdc7b3f8c7cdcb991d8420"
        ),
        "valid": META_INFO(
            os.path.join("simple-examples", "data", "ptb.valid.txt"), "aa0affc06ff7c36e977d7cd49e3839bf"
        ),
        "test": META_INFO(os.path.join("simple-examples", "data", "ptb.test.txt"), "8b80168b89c18661a38ef683c0dc3721"),
    }

    def _get_data(self, mode, **kwargs):
        default_root = os.path.join(DATA_HOME, self.__class__.__name__)
        filename, data_hash = self.SPLITS[mode]
        fullname = os.path.join(default_root, filename)
        if not os.path.exists(fullname) or (data_hash and not md5file(fullname) == data_hash):

            get_path_from_url(self.URL, default_root, self.MD5)

        return fullname

    def _read(self, filename, *args):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line_stripped = line.strip()
                yield {"sentence": line_stripped}
