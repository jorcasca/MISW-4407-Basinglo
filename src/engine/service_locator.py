
from src.engine.services.images_service import ImagesService
from src.engine.services.sounds_service import SoundsService
from src.engine.services.fonts_service import FontsService
from src.engine.services.globals_service import GlobalsService

class ServiceLocator: 
    images_service = ImagesService()
    sounds_service = SoundsService()
    fonts_service = FontsService()
    globals_service = GlobalsService()
