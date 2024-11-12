from .connection import engine
from .models import Base
#from .models.cookie import Cookie
#from .models.interaction_stage import InteractionStage

# Create all tables
Base.metadata.create_all(engine)
