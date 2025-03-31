import pytest
import uuid
from src.domain.entities.user_dto import UserDTO
from src.infrastructure.model.user_model import UserModel
from src.infrastructure.mapper.user_mapper import UserMapper

class TestUserMapper:
    @pytest.fixture
    def sample_user_dto(self):
        return UserDTO(
            id=str(uuid.uuid4()),
            name="Test User",
            phone="3001234567",
            email="test@example.com",
            password="hashedpass",
            salt="salt123",
            role="USER"
        )

    @pytest.fixture
    def sample_user_model(self):
        return UserModel(
            id=str(uuid.uuid4()),
            name="Test User",
            phone="3001234567",
            email="test@example.com",
            password="hashedpass",
            salt="salt123",
            role="USER"
        )

    def test_to_domain(self, sample_user_dto):
        model = UserMapper.to_domain(sample_user_dto)
        assert model is not None
        assert model.id == sample_user_dto.id
        assert model.name == sample_user_dto.name
        assert model.email == sample_user_dto.email

    def test_to_dto(self, sample_user_model):
        dto = UserMapper.to_dto(sample_user_model)
        assert dto is not None
        assert dto.id == sample_user_model.id
        assert dto.name == sample_user_model.name
        assert dto.email == sample_user_model.email