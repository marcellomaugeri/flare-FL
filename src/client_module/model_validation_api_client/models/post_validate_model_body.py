from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_validate_model_body_model import PostValidateModelBodyModel

T = TypeVar("T", bound="PostValidateModelBody")


@_attrs_define
class PostValidateModelBody:
    """
    Attributes:
        model (PostValidateModelBodyModel): The model architecture
        weights (str): The model weights as a base64 encoded string
    """

    model: PostValidateModelBodyModel
    weights: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model = self.model.value

        weights = self.weights

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model": model,
                "weights": weights,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        model = PostValidateModelBodyModel(d.pop("model"))

        weights = d.pop("weights")

        post_validate_model_body = cls(
            model=model,
            weights=weights,
        )

        post_validate_model_body.additional_properties = d
        return post_validate_model_body

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
