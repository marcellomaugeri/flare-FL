from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.post_update_model_body import PostUpdateModelBody
from ...models.post_update_model_response_200 import PostUpdateModelResponse200
from ...models.post_update_model_response_400 import PostUpdateModelResponse400
from ...types import Response


def _get_kwargs(
    *,
    body: PostUpdateModelBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/update_model",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[PostUpdateModelResponse200, PostUpdateModelResponse400]]:
    if response.status_code == 200:
        response_200 = PostUpdateModelResponse200.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = PostUpdateModelResponse400.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[PostUpdateModelResponse200, PostUpdateModelResponse400]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostUpdateModelBody,
) -> Response[Union[PostUpdateModelResponse200, PostUpdateModelResponse400]]:
    """Update model with hex string.

    Args:
        body (PostUpdateModelBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PostUpdateModelResponse200, PostUpdateModelResponse400]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostUpdateModelBody,
) -> Optional[Union[PostUpdateModelResponse200, PostUpdateModelResponse400]]:
    """Update model with hex string.

    Args:
        body (PostUpdateModelBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PostUpdateModelResponse200, PostUpdateModelResponse400]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostUpdateModelBody,
) -> Response[Union[PostUpdateModelResponse200, PostUpdateModelResponse400]]:
    """Update model with hex string.

    Args:
        body (PostUpdateModelBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[PostUpdateModelResponse200, PostUpdateModelResponse400]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    body: PostUpdateModelBody,
) -> Optional[Union[PostUpdateModelResponse200, PostUpdateModelResponse400]]:
    """Update model with hex string.

    Args:
        body (PostUpdateModelBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[PostUpdateModelResponse200, PostUpdateModelResponse400]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
