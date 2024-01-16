from core.database.base import Base
from core.database.models import File, Material, Task, Tool
import datetime
from tests.conftest import engine, test_admin, test_user, TestingSession


# Seed data
creation_time = datetime.datetime(2000, 1, 1, 0, 0, 0)
test_file = File(1, "file_1.gcode", "files/file1.gcode", creation_time)
test_file2 = File(1, "file_2.gcode", "files/file2.gcode", creation_time)
test_file3 = File(2, "file_3.gcode", "files/file3.gcode", creation_time)
test_material = Material("Material 1", "A very useful material", creation_time)
test_material2 = Material("Material 2", "A not so useful material", creation_time)
test_tool = Tool("Tool 1", "A very useful tool", creation_time)
test_tool2 = Tool("Tool 2", "A not so useful tool", creation_time)
test_task1 = Task(1, 1, 1, 1, "Task 1", "A note", "pending_approval", 0, creation_time)
test_task2 = Task(1, 1, 1, 1, "Task 2", "A note", "on_hold", 1, creation_time)
test_task3 = Task(2, 1, 1, 1, "Task 3", "A note", "on_hold", 1, creation_time)


class TestRoutes:
    def setup_class(self):
        # Creates tables in the test database
        Base.metadata.create_all(bind=engine)

        # Seeds the database with test data
        with TestingSession() as session:
            session.add(test_user)
            session.add(test_admin)
            session.add(test_file)
            session.add(test_file2)
            session.add(test_file3)
            session.add(test_material)
            session.add(test_material2)
            session.add(test_tool)
            session.add(test_tool2)
            session.add(test_task1)
            session.add(test_task2)
            session.add(test_task3)
            session.commit()

    def teardown_class(self):
        Base.metadata.drop_all(bind=engine)

# --------------------------------------------------------------------- #
# ------------------------------- USERS ------------------------------- #
# --------------------------------------------------------------------- #

    def test_user_auth(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.get("/users/auth", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {
            'message': 'Successfully authenticated',
            'data': {
                "id": 1,
                "name": "User",
                "email": "user@test.com",
                "role": "user"
            }
        }

    def test_login(self, client):
        data = {"email": "admin@test.com", "password": "password"}

        # Query endpoint under test
        response = client.post("/users/login", json=data)

        # Assertions
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully fetched auth token"

    def test_login_invalid_email(self, client):
        data = {"email": "invalid@test.com", "password": "password"}

        # Query endpoint under test
        response = client.post("/users/login", json=data)

        # Assertions
        assert response.status_code == 404
        assert response.json()["detail"] == "Unauthorized: Invalid email"

    def test_login_invalid_password(self, client):
        data = {"email": "admin@test.com", "password": "invalid-password"}

        # Query endpoint under test
        response = client.post("/users/login", json=data)

        # Assertions
        assert response.status_code == 404
        error_msg = response.json()["detail"]
        assert error_msg == "Unauthorized: Invalid combination of email and password"

    def test_login_db_error(self, client, mocker):
        data = {"email": "admin@test.com", "password": "password"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.userRoutes.UserRepository.get_user_by_email',
            side_effect=Exception('There was an error looking for the user')
        )

        # Query endpoint under test
        response = client.post("/users/login", json=data)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error looking for the user"

    def test_login_token_error(self, client, mocker):
        data = {"email": "admin@test.com", "password": "password"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.userRoutes.generate_token',
            side_effect=Exception('There was an error generating the token')
        )

        # Query endpoint under test
        response = client.post("/users/login", json=data)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error generating the token"

    def test_get_users(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.get("/users/", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                "id": 1,
                "name": "User",
                "email": "user@test.com",
                "role": "user"
            },
            {
                "id": 2,
                "name": "Admin",
                "email": "admin@test.com",
                "role": "admin"
            }
        ]

    def test_create_user(self, client):
        data = {
            "name": "testuser",
            "email": "testuser@nofoobar.com",
            "password": "aVerySecureP@ssw0rd",
            "role": "user"
        }
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.post("/users/", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json()["name"] == "testuser"
        assert response.json()["email"] == "testuser@nofoobar.com"
        assert response.json()["role"] == "user"

    def test_create_user_error(self, client, mocker):
        data = {
            "name": "testuser2",
            "email": "testuser2@nofoobar.com",
            "password": "aVerySecureP@ssw0rd",
            "role": "user"
        }
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.userRoutes.UserRepository.create_user',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.post("/users/", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

    def test_update_user(self, client):
        data = {
            "name": "testupdate",
            "email": "updateduser@nofoobar.com",
            "role": "user"
        }
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.put("/users/3", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"success": "The user was successfully updated"}

    def test_update_user_error(self, client, mocker):
        data = {
            "name": "testupdate",
            "email": "updateduser@nofoobar.com",
            "role": "user"
        }
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.userRoutes.UserRepository.update_user',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.put("/users/3", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

    def test_remove_user(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.delete("/users/3", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"success": "The user was successfully removed"}

    def test_remove_user_error(self, client, mocker):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.userRoutes.UserRepository.remove_user',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.delete("/users/2", headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

# --------------------------------------------------------------------- #
# ------------------------------- FILES ------------------------------- #
# --------------------------------------------------------------------- #

    def test_get_files_from_user(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.get("/files/", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                "id": 1,
                "name": "file_1.gcode",
                "user_id": 1,
                "created_at": "2000-01-01T00:00:00"
            },
            {
                "id": 2,
                "name": "file_2.gcode",
                "user_id": 1,
                "created_at": "2000-01-01T00:00:00"
            }
        ]

    def test_get_all_files(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.get("/files/all", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json() == [
            {
                "id": 1,
                "name": "file_1.gcode",
                "user_id": 1,
                "created_at": "2000-01-01T00:00:00"
            },
            {
                "id": 2,
                "name": "file_2.gcode",
                "user_id": 1,
                "created_at": "2000-01-01T00:00:00"
            },
            {
                "id": 3,
                "name": "file_3.gcode",
                "user_id": 2,
                "created_at": "2000-01-01T00:00:00"
            }
        ]

    def test_create_file(self, client, mocker):
        files = {"file": ("new_file.gcode", b"G54", "text/plain")}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock file validation
        mocker.patch('routes.fileRoutes.validateGcodeFile')

        # Mock FS method to simulate file operation
        mocker.patch('routes.fileRoutes.saveFile')

        # Query endpoint under test
        response = client.post("/files/", files=files, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {'success': 'The file was successfully uploaded'}

    def test_create_file_repeated_name(self, client):
        files = {"file": ("new_file.gcode", b"G55", "text/plain")}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.post("/files/", files=files, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == (
            "Ya existe un archivo con el nombre <<new_file.gcode>>, pruebe renombrarlo"
        )

    def test_create_file_duplicated_content(self, client):
        files = {"file": ("another_file.gcode", b"G54", "text/plain")}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.post("/files/", files=files, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == (
            "El archivo <<new_file.gcode>> tiene el mismo contenido"
        )

    def test_create_file_check_duplicate_db_error(self, client, mocker):
        files = {"file": ("another_file.gcode", b"G55", "text/plain")}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock file validation to simulate exception
        mocker.patch(
            'routes.fileRoutes.FileRepository.check_file_exists',
            side_effect=Exception('There was an error validating the file')
        )

        # Query endpoint under test
        response = client.post("/files/", files=files, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error validating the file"

    def test_create_file_validation_error(self, client, mocker):
        files = {"file": ("another_file.gcode", b"G54 G90", "text/plain")}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock file validation to simulate exception
        mocker.patch(
            'routes.fileRoutes.validateGcodeFile',
            side_effect=Exception('There was an error validating the file')
        )

        # Query endpoint under test
        response = client.post("/files/", files=files, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error validating the file"

    def test_create_file_fs_error(self, client, mocker):
        files = {"file": ("another_file.gcode", b"G54 G90", "text/plain")}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock file validation
        mocker.patch('routes.fileRoutes.validateGcodeFile')

        # Mock FS method to simulate exception
        mocker.patch(
            'routes.fileRoutes.saveFile',
            side_effect=Exception('There was an error saving the file in the FS')
        )

        # Query endpoint under test
        response = client.post("/files/", files=files, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error saving the file in the FS"

    def test_create_file_db_error(self, client, mocker):
        files = {"file": ("another_file.gcode", b"G54 G90", "text/plain")}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock file validation
        mocker.patch('routes.fileRoutes.validateGcodeFile')

        # Mock FS method to simulate file operation
        mocker.patch('routes.fileRoutes.saveFile')

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.fileRoutes.FileRepository.create_file',
            side_effect=Exception('There was an error saving the file in DB')
        )

        # Query endpoint under test
        response = client.post("/files/", files=files, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error saving the file in DB"

    def test_update_file(self, client, mocker):
        data = {"file_name": "updated_file.gcode"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock FS method to simulate file operation
        mocker.patch('routes.fileRoutes.renameFile')

        # Query endpoint under test
        response = client.put("/files/4", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"success": "The file name was successfully updated"}

    def test_update_file_fs_error(self, client, mocker):
        data = {"file_name": "updated_file.gcode"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock FS method to simulate exception
        mocker.patch(
            'routes.fileRoutes.renameFile',
            side_effect=Exception('There was an error updating the file in the FS')
        )

        # Query endpoint under test
        response = client.put("/files/4", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error updating the file in the FS"

    def test_update_file_db_error(self, client, mocker):
        data = {"file_name": "updated_file.gcode"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock FS method to simulate file operation
        mocker.patch('routes.fileRoutes.renameFile')

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.fileRoutes.FileRepository.update_file',
            side_effect=Exception('There was an error updating the file in DB')
        )

        # Query endpoint under test
        response = client.put("/files/1", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error updating the file in DB"

    def test_remove_file(self, client, mocker):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock FS method to simulate file operation
        mocker.patch('routes.fileRoutes.deleteFile')

        # Query endpoint under test
        response = client.delete("/files/4", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"success": "The file was successfully removed"}

    def test_remove_file_fs_error(self, client, mocker):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock FS method to simulate exception
        mocker.patch(
            'routes.fileRoutes.deleteFile',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.delete("/files/2", headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

    def test_remove_file_db_error(self, client, mocker):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock FS method to simulate file operation
        mocker.patch('routes.fileRoutes.deleteFile')

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.fileRoutes.FileRepository.remove_file',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.delete("/files/2", headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

# --------------------------------------------------------------------- #
# ------------------------------- TOOLS ------------------------------- #
# --------------------------------------------------------------------- #

    def test_get_tools(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.get("/tools/", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                "id": 1,
                "name": "Tool 1",
                "description": "A very useful tool",
                "added_at": "2000-01-01T00:00:00"
            },
            {
                "id": 2,
                "name": "Tool 2",
                "description": "A not so useful tool",
                "added_at": "2000-01-01T00:00:00"
            }
        ]

    def test_create_tool(self, client):
        data = {"name": "New tool", "description": "A new tool"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.post("/tools/", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json()["name"] == "New tool"
        assert response.json()["description"] == "A new tool"

    def test_create_tool_error(self, client, mocker):
        data = {"name": "New tool", "description": "Another new tool"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.toolRoutes.ToolRepository.create_tool',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.post("/tools/", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

    def test_update_tool(self, client):
        data = {"name": "Updated tool", "description": "An updated tool"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.put("/tools/3", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"success": "The tool was successfully updated"}

    def test_update_tool_error(self, client, mocker):
        data = {"name": "Updated tool", "description": "An updated tool"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.toolRoutes.ToolRepository.update_tool',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.put("/tools/3", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

    def test_remove_tool(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.delete("/tools/3", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"success": "The tool was successfully removed"}

    def test_remove_tool_error(self, client, mocker):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.toolRoutes.ToolRepository.remove_tool',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.delete("/tools/2", headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

# --------------------------------------------------------------------- #
# ----------------------------- MATERIALS ----------------------------- #
# --------------------------------------------------------------------- #

    def test_get_materials(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.get("/materials/", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                "id": 1,
                "name": "Material 1",
                "description": "A very useful material",
                "added_at": "2000-01-01T00:00:00"
            },
            {
                "id": 2,
                "name": "Material 2",
                "description": "A not so useful material",
                "added_at": "2000-01-01T00:00:00"
            }
        ]

    def test_create_material(self, client):
        data = {"name": "New material", "description": "A new material"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.post("/materials/", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json()["name"] == "New material"
        assert response.json()["description"] == "A new material"

    def test_create_material_error(self, client, mocker):
        data = {"name": "New material", "description": "Another new material"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.materialRoutes.MaterialRepository.create_material',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.post("/materials/", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

    def test_update_material(self, client):
        data = {"name": "Updated material", "description": "An updated material"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.put("/materials/3", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"success": "The material was successfully updated"}

    def test_update_material_error(self, client, mocker):
        data = {"name": "Updated material", "description": "An updated material"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.materialRoutes.MaterialRepository.update_material',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.put("/materials/3", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

    def test_remove_material(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.delete("/materials/3", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {"success": "The material was successfully removed"}

    def test_remove_material_error(self, client, mocker):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.materialRoutes.MaterialRepository.remove_material',
            side_effect=Exception('There was an error')
        )

        # Query endpoint under test
        response = client.delete("/materials/2", headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json()["detail"] == "There was an error"

# --------------------------------------------------------------------- #
# ------------------------------- TASKS ------------------------------- #
# --------------------------------------------------------------------- #

    def test_get_tasks_from_user(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.get("/tasks/", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == [
            {
                "id": 1,
                "name": "Task 1",
                "status": "pending_approval",
                "priority": 0,
                "user_id": 1,
                "file_id": 1,
                "tool_id": 1,
                "material_id": 1,
                "note": "A note",
                "admin_id": None,
                "cancellation_reason": None,
                "created_at": "2000-01-01T00:00:00"
            },
            {
                "id": 2,
                "name": "Task 2",
                "status": "on_hold",
                "priority": 1,
                "user_id": 1,
                "file_id": 1,
                "tool_id": 1,
                "material_id": 1,
                "note": "A note",
                "admin_id": None,
                "cancellation_reason": None,
                "created_at": "2000-01-01T00:00:00"
            }
        ]

    def test_get_all_tasks(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.get("/tasks/all", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert len(response.json()) == 3
        assert response.json() == [
            {
                "id": 1,
                "name": "Task 1",
                "status": "pending_approval",
                "priority": 0,
                "user_id": 1,
                "file_id": 1,
                "tool_id": 1,
                "material_id": 1,
                "note": "A note",
                "admin_id": None,
                "cancellation_reason": None,
                "created_at": "2000-01-01T00:00:00"
            },
            {
                "id": 3,
                "name": "Task 3",
                "status": "on_hold",
                "priority": 1,
                "user_id": 2,
                "file_id": 1,
                "tool_id": 1,
                "material_id": 1,
                "note": "A note",
                "admin_id": None,
                "cancellation_reason": None,
                "created_at": "2000-01-01T00:00:00"
            },
            {
                "id": 2,
                "name": "Task 2",
                "status": "on_hold",
                "priority": 1,
                "user_id": 1,
                "file_id": 1,
                "tool_id": 1,
                "material_id": 1,
                "note": "A note",
                "admin_id": None,
                "cancellation_reason": None,
                "created_at": "2000-01-01T00:00:00"
            }
        ]

    def test_create_task(self, client):
        data = {"file_id": 1, "tool_id": 1, "material_id": 1, "name": "New task", "note": "A note"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.post("/tasks/", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {'success': 'The task was successfully created'}

    def test_create_task_error(self, client, mocker):
        data = {"file_id": 1, "tool_id": 1, "material_id": 1, "name": "New task", "note": "A note"}
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.taskRoutes.TaskRepository.create_task',
            side_effect=Exception('There was an error creating the task in DB')
        )

        # Query endpoint under test
        response = client.post("/tasks/", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json() == {'detail': 'There was an error creating the task in DB'}

    def test_update_task(self, client):
        data = {
            "file_id": 2,
            "tool_id": 2,
            "material_id": 2,
            "name": "Updated task",
            "note": "A new note",
            "priority": 5
        }
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.put("/tasks/4", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {'success': 'The task was successfully updated'}

    def test_update_task_error(self, client, mocker):
        data = {
            "file_id": 2,
            "tool_id": 2,
            "material_id": 2,
            "name": "Updated task",
            "note": "A new note",
            "priority": 5
        }
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.taskRoutes.TaskRepository.update_task',
            side_effect=Exception('There was an error updating the task in DB')
        )

        # Query endpoint under test
        response = client.put("/tasks/4", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json() == {'detail': 'There was an error updating the task in DB'}

    def test_update_task_status(self, client):
        data = {
            "status": "cancelled"
        }
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.put("/tasks/4/status", json=data, headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {'success': 'The task status was successfully updated'}

    def test_update_task_status_error(self, client, mocker):
        data = {
            "status": "on_hold"
        }
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.taskRoutes.TaskRepository.update_task_status',
            side_effect=Exception('There was an error updating the task in DB')
        )

        # Query endpoint under test
        response = client.put("/tasks/4/status", json=data, headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json() == {'detail': 'There was an error updating the task in DB'}

    def test_remove_task(self, client):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Query endpoint under test
        response = client.delete("/tasks/4", headers=headers)

        # Assertions
        assert response.status_code == 200
        assert response.json() == {'success': 'The task was successfully removed'}

    def test_remove_task_error(self, client, mocker):
        headers = {"Authorization": "Bearer a-valid-token"}

        # Mock DB method to simulate exception
        mocker.patch(
            'routes.taskRoutes.TaskRepository.remove_task',
            side_effect=Exception('There was an error removing the task from DB')
        )

        # Query endpoint under test
        response = client.delete("/tasks/3", headers=headers)

        # Assertions
        assert response.status_code == 400
        assert response.json() == {'detail': 'There was an error removing the task from DB'}
