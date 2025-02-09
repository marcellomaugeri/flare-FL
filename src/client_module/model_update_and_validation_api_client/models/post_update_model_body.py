from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_update_model_body_model_id import PostUpdateModelBodyModelId

T = TypeVar("T", bound="PostUpdateModelBody")


@_attrs_define
class PostUpdateModelBody:
    """
    Attributes:
        model_id (PostUpdateModelBodyModelId):
        hex_weights (str):
    """

    model_id: PostUpdateModelBodyModelId
    hex_weights: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id.value

        hex_weights = self.hex_weights

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model_id": model_id,
                "hex_weights": hex_weights,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        model_id = PostUpdateModelBodyModelId(d.pop("model_id"))

        hex_weights = d.pop("hex_weights")

        post_update_model_body = cls(
            model_id=model_id,
            hex_weights=hex_weights,
        )

        post_update_model_body.additional_properties = d
        return post_update_model_body

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
