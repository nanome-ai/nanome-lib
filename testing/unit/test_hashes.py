import unittest
from nanome.api._hashes import Hashes


class HashesTestCase(unittest.TestCase):
    """Ensure that Hash values remain constant."""

    def setUp(self):
        Hashes.init_hashes()

    def test_integration_hashes(self):
        expected_hashes = [
            287474962, 287492584, 660242612, 103842316,
            446505985, 446505999, 183504179, 240792748,
            183513874, 317731250, 183510640, 317728368
        ]
        self.assertEqual(Hashes.IntegrationHashes, expected_hashes)

    def test_command_hashes(self):
        expected_hashes = [
            116013167, 623462994, 34786951, 458731680, 88085588, 88102996, 641741420, 692757664,
            692329632, 641729705, 309874085, 309596192, 309925025, 151758252, 458837586, 783319662,
            118236179, 118227566, 658166803, 660262048, 33573381, 546819765, 118231532, 118232783,
            71336399, 151130291, 118243971, 643072037, 117606532, 642782383, 642782849, 642782341,
            642798164, 139952750, 206748844, 206602697, 183513107, 552316137, 120081541, 422071909,
            455626437, 120081925, 235518176, 537508352, 623398309, 614023789, 446251627, 234998959,
            604078708, 557449426, 557449253, 122047059, 637567604, 139461651, 33953249, 407142863, 307281351]
        self.assertEqual(Hashes.CommandHashes, expected_hashes)

    def test_message_hashes(self):
        expected_hashes = [
            116013167, 544230484, 458772640, 122307215, 475550176, 458837587, 458837586,
            479306766, 280265803, 660262048, 660262156, 660262387, 660262053, 783319173, 783319603, 33573381,
            118227507, 118236177, 658166801, 71338113, 151145476, 280473604, 280137187, 117606543, 642782386,
            642782849, 642797044, 139952691, 206738629, 206608545, 183513263, 552316137, 104960100, 422989203,
            459725238, 242457831, 554189328, 618214989, 613861522, 446023821, 117555312, 642825933, 139463813,
            604096515, 654360045, 234999425, 557449426, 122047059, 637586433, 139461765, 33952911, 518602764,
            407154825, 307281351, 638378635, 46251621]
        self.assertEqual(Hashes.MessageHashes, expected_hashes)

    def test_integration_request_hashes(self):
        expected_hashes = [
            287499758, 660242612, 103842316, 446506409, 183513874, 183504179, 240792748, 317731250,
            46447411, 307346725, 650752620
        ]
        self.assertEqual(Hashes.IntegrationRequestHashes, expected_hashes)

    def test_permission_request_hashes(self):
        expected_hashes = [403903525]
        self.assertEqual(Hashes.PermissionRequestHashes, expected_hashes)

    def test_has_to_integration_name(self):
        expected_dict = {
            287474962: 'hydrogen_add',
            287492584: 'hydrogen_remove',
            660242612: 'structure_prep',
            103842316: 'calculate_esp',
            446505985: 'minimization_start',
            446505999: 'minimization_stop',
            183504179: 'export_locations',
            240792748: 'generate_molecule_image',
            183513874: 'export_file',
            317731250: 'import_file',
            183510640: 'export_smiles',
            317728368: 'import_smiles'
        }
        self.assertEqual(Hashes.HashToIntegrationName, expected_dict)
