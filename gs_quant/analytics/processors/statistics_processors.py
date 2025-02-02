"""
Copyright 2019 Goldman Sachs.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
KIND, either express or implied.  See the License for the
specific language governing permissions and limitations
under the License.
"""

from typing import Optional, Union

from gs_quant.analytics.core.processor import BaseProcessor, DataCoordinateOrProcessor, DateOrDatetimeOrRDate
from gs_quant.analytics.core.processor_result import ProcessorResult
from gs_quant.timeseries import percentiles, Window


class PercentilesProcessor(BaseProcessor):
    def __init__(self,
                 a: DataCoordinateOrProcessor,
                 *,
                 b: Optional[DataCoordinateOrProcessor] = None,
                 start: Optional[DateOrDatetimeOrRDate] = None,
                 end: Optional[DateOrDatetimeOrRDate] = None,
                 w: Union[Window, int] = Window(None, 0)):
        """ PercentilesProcessor

        :param a: DataCoordinate or BaseProcessor for the first series
        :param b: DataCoordinate or BaseProcessor for the second series
        :param start: start date or time used in the underlying data query
        :param end: end date or time used in the underlying data query
        :param w:  Window or int: size of window and ramp up to use. e.g. Window(22, 10) where 22 is the window size
              and 10 the ramp up value.  If w is a string, it should be a relative date like '1m', '1d', etc.
              Window size defaults to length of series.
        """
        super().__init__()
        self.children['a'] = a
        self.children['b'] = b

        self.start = start
        self.end = end
        self.w = w

    def process(self):
        a_data = self.children_data.get('a')
        if isinstance(a_data, ProcessorResult):
            if a_data.success:
                b_data = self.children_data.get('b')
                # Need to check if the child node b was set in the first place.
                if self.children.get('b') and isinstance(b_data, ProcessorResult):
                    if b_data.success:
                        result = percentiles(a_data.data, b_data.data, w=self.w)
                        self.value = ProcessorResult(True, result)
                    else:
                        self.value = ProcessorResult(True, 'PercentilesProcessor: b is not a valid series.')
                result = percentiles(a_data.data, w=self.w)
                self.value = ProcessorResult(True, result)

    def get_plot_expression(self):
        pass
