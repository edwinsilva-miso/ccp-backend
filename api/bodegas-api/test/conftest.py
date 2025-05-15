import pytest
from unittest.mock import MagicMock, patch

from src.domain.entities.warehouse_dto import WarehouseDTO
from src.domain.entities.warehouse_stock_item_dto import WarehouseStockItemDTO
from src.infrastructure.adapters.warehouse_adapter import WarehouseAdapter
from src.infrastructure.adapters.warehouse_stock_item_adapter import WarehouseStockItemAdapter
from src.infrastructure.database.declarative_base import Base, engine
# Import models to ensure tables are created
from src.infrastructure.model.warehouse_model import WarehouseModel
from src.infrastructure.model.warehouse_stock_item_model import WarehouseStockItemModel

# Create all tables in the test database
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create all tables in the test database before tests run"""
    Base.metadata.create_all(engine)
    yield
    # Drop all tables after tests are done
    Base.metadata.drop_all(engine)


@pytest.fixture
def warehouse_dto():
    """Fixture for a sample warehouse DTO"""
    return WarehouseDTO(
        warehouse_id="w123",
        location="Test Location",
        description="Test Description",
        name="Test Warehouse",
        administrator_id="admin123",
        status="active",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00"
    )


@pytest.fixture
def warehouse_dto_list():
    """Fixture for a list of warehouse DTOs"""
    return [
        WarehouseDTO(
            warehouse_id="w123",
            location="Test Location 1",
            description="Test Description 1",
            name="Test Warehouse 1",
            administrator_id="admin123",
            status="active",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00"
        ),
        WarehouseDTO(
            warehouse_id="w456",
            location="Test Location 2",
            description="Test Description 2",
            name="Test Warehouse 2",
            administrator_id="admin456",
            status="inactive",
            created_at="2023-01-02T00:00:00",
            updated_at="2023-01-02T00:00:00"
        )
    ]


@pytest.fixture
def warehouse_stock_item_dto():
    """Fixture for a sample warehouse stock item DTO"""
    return WarehouseStockItemDTO(
        warehouse_stock_item_id="wsi123",
        warehouse_id="w123",
        item_id="item123",
        bar_code="12345678",
        identification_code="ID12345",
        width=10.0,
        height=20.0,
        depth=30.0,
        weight=5.0,
        hallway="A",
        shelf="1",
        sold=False,
        status="active",
        created_at="2023-01-01T00:00:00",
        updated_at="2023-01-01T00:00:00"
    )


@pytest.fixture
def warehouse_stock_item_dto_list():
    """Fixture for a list of warehouse stock item DTOs"""
    return [
        WarehouseStockItemDTO(
            warehouse_stock_item_id="wsi123",
            warehouse_id="w123",
            item_id="item123",
            bar_code="12345678",
            identification_code="ID12345",
            width=10.0,
            height=20.0,
            depth=30.0,
            weight=5.0,
            hallway="A",
            shelf="1",
            sold=False,
            status="active",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00"
        ),
        WarehouseStockItemDTO(
            warehouse_stock_item_id="wsi456",
            warehouse_id="w123",
            item_id="item456",
            bar_code="87654321",
            identification_code="ID54321",
            width=15.0,
            height=25.0,
            depth=35.0,
            weight=7.5,
            hallway="B",
            shelf="2",
            sold=True,
            status="inactive",
            created_at="2023-01-02T00:00:00",
            updated_at="2023-01-02T00:00:00"
        )
    ]


@pytest.fixture
def mock_warehouse_dao():
    """Fixture for mocking WarehouseDAO"""
    with patch('src.infrastructure.dao.warehouse_dao.WarehouseDAO') as mock:
        yield mock


@pytest.fixture
def mock_warehouse_mapper():
    """Fixture for mocking WarehouseMapper"""
    with patch('src.infrastructure.mapper.warehouse_mapper.WarehouseMapper') as mock:
        yield mock


@pytest.fixture
def mock_warehouse_stock_item_dao():
    """Fixture for mocking WarehouseStockItemDAO"""
    with patch('src.infrastructure.dao.warehouse_stock_item_dao.WarehouseStockItemDAO') as mock:
        yield mock


@pytest.fixture
def mock_warehouse_stock_item_mapper():
    """Fixture for mocking WarehouseStockItemMapper"""
    with patch('src.infrastructure.mapper.warehouse_stock_item_mapper.WarehouseStockItemMapper') as mock:
        yield mock


@pytest.fixture
def warehouse_adapter(mock_warehouse_dao, mock_warehouse_mapper):
    """Fixture for WarehouseAdapter with mocked dependencies"""
    return WarehouseAdapter()


@pytest.fixture
def warehouse_stock_item_adapter(mock_warehouse_stock_item_dao, mock_warehouse_stock_item_mapper):
    """Fixture for WarehouseStockItemAdapter with mocked dependencies"""
    return WarehouseStockItemAdapter()
