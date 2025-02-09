from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_validate_response_200 import GetValidateResponse200
from ...models.get_validate_response_400 import GetValidateResponse400
from ...models.get_validate_response_409 import GetValidateResponse409
from ...types import UNSET, Response


def _get_kwargs(
    *,
    model_id: str,
    update_id: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["model_id"] = model_id

    params["update_id"] = update_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/validate",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]]:
    if response.status_code == 200:
        response_200 = GetValidateResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = GetValidateResponse400.from_dict(response.json())

        return response_400
    if response.status_code == 409:
        response_409 = GetValidateResponse409.from_dict(response.json())

        return response_409
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    model_id: str,
    update_id: str,
) -> Response[Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]]:
    """Validate model update.

    Args:
        model_id (str):
        update_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]]
    """

    kwargs = _get_kwargs(
        model_id=model_id,
        update_id=update_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    model_id: str,
    update_id: str,
) -> Optional[Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]]:
    """Validate model update.

    Args:
        model_id (str):
        update_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]
    """

    return sync_detailed(
        client=client,
        model_id=model_id,
        update_id=update_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    model_id: str,
    update_id: str,
) -> Response[Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]]:
    """Validate model update.

    Args:
        model_id (str):
        update_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]]
    """

    kwargs = _get_kwargs(
        model_id=model_id,
        update_id=update_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    model_id: str,
    update_id: str,
) -> Optional[Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]]:
    """Validate model update.

    Args:
        model_id (str):
        update_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetValidateResponse200, GetValidateResponse400, GetValidateResponse409]
    """

    return (
        await asyncio_detailed(
            client=client,
            model_id=model_id,
            update_id=update_id,
        )
    ).parsed
