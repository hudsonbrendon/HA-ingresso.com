"""Cliente da API Ingresso.com."""

from __future__ import annotations

import logging
import socket
from typing import Any

import aiohttp
import async_timeout

from .const import BASE_URL, THEATER_URL

_LOGGER = logging.getLogger(__name__)


class IngressoApiClientError(Exception):
    """Exceção para indicar um erro geral na API."""


class IngressoApiClientCommunicationError(IngressoApiClientError):
    """Exceção para indicar um erro de comunicação."""


class IngressoApiClientAuthenticationError(IngressoApiClientError):
    """Exceção para indicar um erro de autenticação."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verificar se a resposta é válida."""
    if response.status in (401, 403):
        msg = "Credenciais inválidas"
        raise IngressoApiClientAuthenticationError(msg)
    response.raise_for_status()


class IngressoApiClient:
    """Cliente da API Ingresso.com."""

    def __init__(
        self,
        city_id: int,
        partnership: str,
        session: aiohttp.ClientSession,
        theater: str = None,
    ) -> None:
        """Inicializar cliente da API Ingresso.com."""
        self._city_id = city_id
        self._partnership = partnership
        self._session = session
        self._theater = theater

    async def async_get_movies(self) -> Any:
        """Obter dados de filmes da API."""
        if self._theater:
            url = THEATER_URL.format(self._city_id, self._partnership, self._theater)
        else:
            url = BASE_URL.format(self._city_id, self._partnership)

        return await self._api_wrapper(
            method="get",
            url=url,
            headers={"User-Agent": "Mozilla/5.0"},
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Obter informações da API."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            msg = f"Erro de tempo limite ao buscar informações - {exception}"
            raise IngressoApiClientCommunicationError(msg) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            msg = f"Erro ao buscar informações - {exception}"
            raise IngressoApiClientCommunicationError(msg) from exception
        except Exception as exception:  # pylint: disable=broad-except
            msg = f"Algo realmente errado aconteceu! - {exception}"
            raise IngressoApiClientError(msg) from exception
