import unittest
from unittest.mock import MagicMock, patch

from api.usuarios_api.src.application.find_user_by_role import FindUserByRole
from api.usuarios_api.src.domain.entities.user_dto import UserDTO


class TestFindUserByRole(unittest.TestCase):

    def setUp(self):
        # Crear mock del repositorio de usuarios
        self.user_repository_mock = MagicMock()

        # Instanciar el caso de uso con el mock
        self.find_user_by_role = FindUserByRole(self.user_repository_mock)

    def test_execute_returns_list_of_users_with_specified_role(self):
        # Arrange
        role_name = "CLIENTE"

        # Crear usuarios de prueba
        mock_users = [
            UserDTO(
                id="1",
                name="Usuario Admin 1",
                phone="1234567890",
                email="admin1@example.com",
                password="hashedpass1",
                token=None,
                salt="salt1",
                role="CLIENTE",
                expire_at=None
            ),
            UserDTO(
                id="2",
                name="Usuario Admin 2",
                phone="0987654321",
                email="admin2@example.com",
                password="hashedpass2",
                token=None,
                salt="salt2",
                role="CLIENTE",
                expire_at=None
            )
        ]

        # Configurar el mock para devolver los usuarios cuando se llame a find_by_role
        self.user_repository_mock.find_by_role.return_value = mock_users

        # Act
        result = self.find_user_by_role.execute(role_name)

        # Assert
        self.user_repository_mock.find_by_role.assert_called_once_with(role_name)
        #self.assertEqual(len(result), 2)

        # Verificar que el formato de respuesta es correcto
        self.assertEqual(result[0]['id'], "1")
        self.assertEqual(result[0]['name'], "Usuario Admin 1")
        self.assertEqual(result[0]['phone'], "1234567890")
        self.assertEqual(result[0]['email'], "admin1@example.com")
        self.assertEqual(result[0]['role'], "CLIENTE")

        self.assertEqual(result[1]['id'], "2")
        self.assertEqual(result[1]['name'], "Usuario Admin 2")
        self.assertEqual(result[1]['phone'], "0987654321")
        self.assertEqual(result[1]['email'], "admin2@example.com")
        self.assertEqual(result[1]['role'], "CLIENTE")

    def test_execute_returns_empty_list_when_no_users_found(self):
        # Arrange
        role_name = "CLIENT"

        # Configurar el mock para devolver una lista vacía
        self.user_repository_mock.find_by_role.return_value = []

        # Act
        result = self.find_user_by_role.execute(role_name)

        # Assert
        self.user_repository_mock.find_by_role.assert_called_once_with(role_name)
        #self.assertEqual(len(result), 0)
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()