from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_validate_model_model import GetValidateModelModel
from ...models.get_validate_model_response_200 import GetValidateModelResponse200
from ...types import UNSET, Response


def _get_kwargs(
    *,
    model: GetValidateModelModel,
    weights: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_model = model.value
    params["model"] = json_model

    params["weights"] = weights

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/validate_model",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetValidateModelResponse200]:
    if response.status_code == 200:
        response_200 = GetValidateModelResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetValidateModelResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    model: GetValidateModelModel,
    weights: str,
) -> Response[GetValidateModelResponse200]:
    """Validate the model with provided weights

    Args:
        model (GetValidateModelModel):
        weights (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetValidateModelResponse200]
    """

    kwargs = _get_kwargs(
        model=model,
        weights=weights,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    model: GetValidateModelModel,
    weights: str,
) -> Optional[GetValidateModelResponse200]:
    """Validate the model with provided weights

    Args:
        model (GetValidateModelModel):
        weights (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetValidateModelResponse200
    """

    return sync_detailed(
        client=client,
        model=model,
        weights=weights,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    model: GetValidateModelModel,
    weights: str,
) -> Response[GetValidateModelResponse200]:
    """Validate the model with provided weights

    Args:
        model (GetValidateModelModel):
        weights (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetValidateModelResponse200]
    """

    kwargs = _get_kwargs(
        model=model,
        weights=weights,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    model: GetValidateModelModel,
    weights: str,
) -> Optional[GetValidateModelResponse200]:
    """Validate the model with provided weights

    Args:
        model (GetValidateModelModel):
        weights (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetValidateModelResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            model=model,
            weights=weights,
        )
    ).parsed
