from . import orders, order_details, recipes, sandwiches, resources

from ..dependencies.database import Base, engine


def index():
    # Uses all bases in classes to create all tables
    Base.metadata.create_all(bind=engine)
    ### orders.Base.metadata.create_all(engine)
    ### order_details.Base.metadata.create_all(engine)
    ### recipes.Base.metadata.create_all(engine)
    ### sandwiches.Base.metadata.create_all(engine)
    ### resources.Base.metadata.create_all(engine) 
