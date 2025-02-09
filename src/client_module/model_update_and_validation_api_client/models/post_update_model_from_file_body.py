from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.post_update_model_from_file_body_model_id import PostUpdateModelFromFileBodyModelId

T = TypeVar("T", bound="PostUpdateModelFromFileBody")


@_attrs_define
class PostUpdateModelFromFileBody:
    """
    Attributes:
        model_id (PostUpdateModelFromFileBodyModelId):
        file_path (str):
    """

    model_id: PostUpdateModelFromFileBodyModelId
    file_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        model_id = self.model_id.value

        file_path = self.file_path

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "model_id": model_id,
                "file_path": file_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        model_id = PostUpdateModelFromFileBodyModelId(d.pop("model_id"))

        file_path = d.pop("file_path")

        post_update_model_from_file_body = cls(
            model_id=model_id,
            file_path=file_path,
        )

        post_update_model_from_file_body.additional_properties = d
        return post_update_model_from_file_body

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
