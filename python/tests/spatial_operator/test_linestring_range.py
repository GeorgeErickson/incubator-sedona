#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.

import os

from pyspark import StorageLevel

from geospark.core.SpatialRDD import LineStringRDD
from geospark.core.enums import IndexType, FileDataSplitter
from geospark.core.geom.envelope import Envelope
from geospark.core.spatialOperator import RangeQuery
from tests.test_base import TestBase
from tests.tools import tests_path

input_location = os.path.join(tests_path, "resources/primaryroads-linestring.csv")
offset = 0
splitter = FileDataSplitter.CSV
gridType = "rtree"
indexType = "rtree"


class TestLineStringRange(TestBase):
    loop_times = 5
    query_envelope = Envelope(-85.01, -60.01, 34.01, 50.01)

    def test_spatial_range_query(self):
        spatial_rdd = LineStringRDD(
            self.sc, input_location, splitter, True, StorageLevel.MEMORY_ONLY
        )
        for i in range(self.loop_times):
            result_size = RangeQuery.SpatialRangeQuery(spatial_rdd, self.query_envelope, False, False).count()
            assert result_size == 999

        assert RangeQuery.SpatialRangeQuery(
            spatial_rdd, self.query_envelope, False, False).take(10)[1].getUserData() is not None

    def test_spatial_range_query_using_index(self):
        spatial_rdd = LineStringRDD(
            self.sc, input_location, splitter, True, StorageLevel.MEMORY_ONLY
        )
        spatial_rdd.buildIndex(IndexType.RTREE, False)

        for i in range(self.loop_times):
            result_size = RangeQuery.SpatialRangeQuery(spatial_rdd, self.query_envelope, False, False).count()
            assert result_size == 999

        assert RangeQuery.SpatialRangeQuery(
            spatial_rdd, self.query_envelope, False, False).take(10)[1].getUserData() is not None
