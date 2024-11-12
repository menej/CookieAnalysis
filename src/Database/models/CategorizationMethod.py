from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from . import Base

class WebsiteCrawl(Base):
    __tablename__ = 'website_crawls'

    id = Column(Integer, primary_key=True)
    website_id = Column(Integer, ForeignKey('websites.id'))
    performance_state_id = Column(Integer, ForeignKey('performance_states.id'))
    processing_mechanism_id = Column(Integer, ForeignKey('processing_mechanisms.id'))

    website = relationship('Website', back_populates='crawls')
    state = relationship('PerformanceState', back_populates='crawls')
    mechanism = relationship('ProcessingMechanism', back_populates='crawls')
