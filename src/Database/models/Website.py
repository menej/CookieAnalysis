from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from . import Base

class Website(Base):
    __tablename__ = 'websites'

    id = Column(Integer, primary_key=True)
    url = Column(String(255), nullable=False)
    description = Column(String(512), nullable=True)

    crawls = relationship('WebsiteCrawl', back_populates='website')
