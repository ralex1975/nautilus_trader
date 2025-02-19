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

import asyncio

import pytest

from nautilus_trader.adapters.betfair.sockets import BetfairMarketStreamClient
from nautilus_trader.adapters.betfair.sockets import BetfairOrderStreamClient
from nautilus_trader.adapters.betfair.sockets import BetfairStreamClient
from nautilus_trader.common.clock import LiveClock
from nautilus_trader.common.logging import Logger
from nautilus_trader.common.logging import LoggerAdapter
from tests.integration_tests.adapters.betfair.test_kit import BetfairTestStubs


class TestBetfairSockets:
    def setup(self):
        # Fixture Setup
        self.loop = asyncio.get_event_loop()
        self.clock = LiveClock()
        self.logger = Logger(clock=self.clock, bypass=True)
        self.client = BetfairTestStubs.betfair_client(loop=self.loop, logger=self.logger)

    def _build_stream_client(self, host: str, port: int, handler) -> BetfairStreamClient:
        client = BetfairStreamClient(
            http_client=self.client,
            logger_adapter=LoggerAdapter("bf", self.logger),
            message_handler=handler,
            host=host,
            port=port,
        )
        client.use_ssl = False
        return client

    def test_unique_id(self):
        clients = [
            BetfairMarketStreamClient(
                http_client=self.client,
                logger=self.logger,
                message_handler=len,
            ),
            BetfairOrderStreamClient(
                http_client=self.client,
                logger=self.logger,
                message_handler=len,
            ),
            BetfairMarketStreamClient(
                http_client=self.client,
                logger=self.logger,
                message_handler=len,
            ),
        ]
        result = [c.unique_id for c in clients]
        assert result == sorted(set(result))

    @pytest.mark.asyncio
    async def test_socket_client_connect(self, socket_server):
        # Arrange
        messages = []
        host, port = socket_server
        client = self._build_stream_client(host=host, port=port, handler=messages.append)

        # Act
        await client.connect()

        # Assert
        assert client.is_connected
        await client.disconnect()

    @pytest.mark.asyncio
    async def test_socket_client_reconnect(self, closing_socket_server):
        # Arrange
        messages = []
        host, port = closing_socket_server
        client = self._build_stream_client(host=host, port=port, handler=messages.append)

        # Act
        await client.connect()
        await asyncio.sleep(2)

        # Assert
        assert client.is_connected
        await client.disconnect()
