# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2023 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------
from nautilus_trader.core.nautilus_pyo3 import Equity
from nautilus_trader.test_kit.rust.instruments import TestInstrumentProviderPyo3


aapl_equity = TestInstrumentProviderPyo3.appl_equity()


def test_equality():
    item_1 = TestInstrumentProviderPyo3.appl_equity()
    item_2 = TestInstrumentProviderPyo3.appl_equity()
    assert item_1 == item_2


def test_hash():
    assert hash(aapl_equity) == hash(aapl_equity)


def test_to_dict():
    dict = aapl_equity.to_dict()
    assert Equity.from_dict(dict) == aapl_equity
    assert dict == {
        "type": "Equity",
        "id": "AAPL.NASDAQ",
        "raw_symbol": "AAPL",
        "isin": "US0378331005",
        "currency": "USD",
        "price_precision": 2,
        "price_increment": "0.01",
        "multiplier": "1",
        "margin_init": 0.0,
        "margin_maint": 0.0,
        "maker_fee": 0.001,
        "taker_fee": 0.001,
        "lot_size": "1.0",
        "max_quantity": None,
        "min_quantity": None,
        "max_price": None,
        "min_price": None,
    }
