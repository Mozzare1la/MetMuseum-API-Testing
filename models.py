from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class Item(BaseModel):
    objectID: int
    isHighlight: bool
    accessionNumber: str
    accessionYear: str
    isPublicDomain: bool
    primaryImage: str
    primaryImage: str
    additionalImages: list[str]
    constituents: Optional[list[dict[str, int | str]]] = None
    department: str
    objectName: str
    title: str
    culture: str
    period: str
    dynasty: str
    reign: str
    portfolio: str
    artistRole: str
    artistPrefix: str
    artistDisplayName: str
    artistDisplayBio: str
    artistSuffix: str
    artistAlphaSort: str
    artistNationality: str
    artistBeginDate: str
    artistEndDate: str
    artistGender: str
    artistWikidata_URL: str
    artistULAN_URL: str
    objectDate: str
    objectBeginDate: int
    objectEndDate: int
    medium: str
    dimensions: str
    dimensionsParsed: Optional[list[dict[str, str | float]]] = None
    measurements: Optional[list] = None
    creditLine: str
    geographyType: str
    city: str
    state: str
    county: str
    country: str
    region: str
    subregion: str
    locale: str
    locus: str
    excavation: str
    river: str
    classification: str
    rightsAndReproduction: str
    linkResource: str
    metadataDate: datetime = None
    repository: str
    objectURL: str
    tags: Optional[list[dict[str, str]]] = None
    objectWikidata_URL: str
    isTimelineWork: bool
    GalleryNumber: str

class SearchResults(BaseModel):
   total: int
   objectIDs: Optional[list[int]] = None 
