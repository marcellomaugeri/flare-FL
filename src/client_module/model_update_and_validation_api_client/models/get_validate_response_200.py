from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetValidateResponse200")


@_attrs_define
class GetValidateResponse200:
    """
    Attributes:
        model_id (Union[Unset, str]): The model ID.
        update_id (Union[Unset, str]): The update ID (SHA256 hash).
    """

    model_id: Union[Unset, str] = UNSET
    update_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id

        update_id = self.update_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if model_id is not UNSET:
            field_dict["model_id"] = model_id
        if update_id is not UNSET:
            field_dict["update_id"] = update_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        model_id = d.pop("model_id", UNSET)

        update_id = d.pop("update_id", UNSET)

        get_validate_response_200 = cls(
            model_id=model_id,
            update_id=update_id,
        )

        get_validate_response_200.additional_properties = d
        return get_validate_response_200

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
