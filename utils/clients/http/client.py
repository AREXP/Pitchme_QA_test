import typing

from requests import Session, Response, Request
from utils.types import (AuthTypes, CookieTypes, HeaderTypes, QueryParamTypes,
                         RequestContent, RequestData, RequestExtensions,
                         RequestFiles, TimeoutTypes, URLTypes)


class HTTPClient(Request):

    def get(
            self,
            url: URLTypes,
            *,
            params: typing.Optional[QueryParamTypes] = None,
            headers: typing.Optional[HeaderTypes] = None,
            cookies: typing.Optional[CookieTypes] = None,
            auth: typing.Union[AuthTypes, Session] = None,
            follow_redirects: typing.Union[bool, Session] = None,
            timeout: typing.Union[TimeoutTypes, Session] = None,
            extensions: typing.Optional[RequestExtensions] = None
    ) -> Response:
        return super().get(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions
        )

    def post(
            self,
            url: URLTypes,
            *,
            content: typing.Optional[RequestContent] = None,
            data: typing.Optional[RequestData] = None,
            files: typing.Optional[RequestFiles] = None,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[QueryParamTypes] = None,
            headers: typing.Optional[HeaderTypes] = None,
            cookies: typing.Optional[CookieTypes] = None,
            auth: typing.Union[AuthTypes, Session] = None,
            follow_redirects: typing.Union[bool, Session] = None,
            timeout: typing.Union[TimeoutTypes, Session] = None,
            extensions: typing.Optional[RequestExtensions] = None
    ) -> Response:
        return super().post(
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions
        )

    def put(
            self,
            url: URLTypes,
            *,
            content: typing.Optional[RequestContent] = None,
            data: typing.Optional[RequestData] = None,
            files: typing.Optional[RequestFiles] = None,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[QueryParamTypes] = None,
            headers: typing.Optional[HeaderTypes] = None,
            cookies: typing.Optional[CookieTypes] = None,
            auth: typing.Union[AuthTypes, Session] = None,
            follow_redirects: typing.Union[bool, Session] = None,
            timeout: typing.Union[TimeoutTypes, Session] = None,
            extensions: typing.Optional[RequestExtensions] = None
    ) -> Response:
        return super().put(
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions
        )

    def delete(
            self,
            url: URLTypes,
            *,
            params: typing.Optional[QueryParamTypes] = None,
            headers: typing.Optional[HeaderTypes] = None,
            cookies: typing.Optional[CookieTypes] = None,
            auth: typing.Union[AuthTypes, Session] = None,
            follow_redirects: typing.Union[bool, Session] = None,
            timeout: typing.Union[TimeoutTypes, Session] = None,
            extensions: typing.Optional[RequestExtensions] = None
    ) -> Response:
        return super().delete(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions
        )


class APIClient:
    def __init__(self, client: HTTPClient) -> None:
        self._client = client

    @property
    def client(self) -> HTTPClient:
        return self._client
