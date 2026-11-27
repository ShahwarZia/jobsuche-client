"""Pydantic models for the Bundesagentur für Arbeit Jobsuche API.

The API uses German keys. Models expose English snake_case names and map the
German keys via ``validation_alias``. Unmodelled keys are ignored.
"""

from datetime import date, datetime

from pydantic import AliasPath, BaseModel, ConfigDict, Field


class _BaseModel(BaseModel):
    """Shared config: accept German aliases and English names, ignore extras."""

    model_config = ConfigDict(validate_by_name=True, extra="ignore")


class Address(_BaseModel):
    """Postal address of a job location (``stellenlokationen[].adresse``)."""

    postal_code: str | None = Field(default=None, validation_alias="plz")
    city: str | None = Field(default=None, validation_alias="ort")
    street: str | None = Field(default=None, validation_alias="strasse")
    house_number: str | None = Field(default=None, validation_alias="hausnummer")
    region: str | None = Field(default=None, validation_alias="region")
    country: str | None = Field(default=None, validation_alias="land")


class Location(_BaseModel):
    """One job location with address and coordinates (``stellenlokationen[]``)."""

    address: Address | None = Field(default=None, validation_alias="adresse")
    latitude: float | None = Field(default=None, validation_alias="breite")
    longitude: float | None = Field(default=None, validation_alias="laenge")


class JobBase(_BaseModel):
    """Fields shared by search result items and job details."""

    reference_number: str = Field(validation_alias="referenznummer")
    title: str = Field(validation_alias="stellenangebotsTitel")
    employer: str = Field(validation_alias="firma")
    offer_type: str = Field(validation_alias="stellenangebotsart")

    main_occupation: str | None = Field(default=None, validation_alias="hauptberuf")
    locations: list[Location] = Field(
        default_factory=list, validation_alias="stellenlokationen"
    )

    published_from: date | None = Field(
        default=None, validation_alias=AliasPath("veroeffentlichungszeitraum", "von")
    )
    start_date: date | None = Field(
        default=None, validation_alias=AliasPath("eintrittszeitraum", "von")
    )
    first_published: date | None = Field(
        default=None, validation_alias="datumErsteVeroeffentlichung"
    )
    modified_at: datetime | None = Field(
        default=None, validation_alias="aenderungsdatum"
    )

    salary_info: str | None = Field(default=None, validation_alias="verguetungsangabe")
    contract_duration: str | None = Field(
        default=None, validation_alias="vertragsdauer"
    )

    full_time: bool | None = Field(default=None, validation_alias="arbeitszeitVollzeit")
    part_time_morning: bool | None = Field(
        default=None, validation_alias="arbeitszeitTeilzeitVormittag"
    )
    part_time_afternoon: bool | None = Field(
        default=None, validation_alias="arbeitszeitTeilzeitNachmittag"
    )
    part_time_evening: bool | None = Field(
        default=None, validation_alias="arbeitszeitTeilzeitAbend"
    )
    part_time_flexible: bool | None = Field(
        default=None, validation_alias="arbeitszeitTeilzeitFlexibel"
    )
    shift_night_weekend: bool | None = Field(
        default=None, validation_alias="arbeitszeitSchichtNachtWochenende"
    )

    remote_possible: bool | None = Field(
        default=None, validation_alias="homeofficemoeglich"
    )
    career_changer_suitable: bool | None = Field(
        default=None, validation_alias="quereinstiegGeeignet"
    )
    marginal_employment: bool | None = Field(
        default=None, validation_alias="istGeringfuegigeBeschaeftigung"
    )
    external_url: str | None = Field(default=None, validation_alias="externeURL")


class JobSummary(JobBase):
    """One item of a search response (``ergebnisliste[]``)."""

    distance_km: int | None = Field(default=None, validation_alias="entfernung")
    occupations: list[str] = Field(default_factory=list, validation_alias="alleBerufe")
    salary_type: str | None = Field(default=None, validation_alias="artDerVerguetung")
    salary_min: float | None = Field(default=None, validation_alias="gehaltsspanneVon")
    salary_max: float | None = Field(default=None, validation_alias="gehaltsspanneBis")
    remote_type: str | None = Field(default=None, validation_alias="homeofficetyp")
    remote_percent: int | None = Field(
        default=None, validation_alias="homeofficeprozent"
    )


class SearchResult(_BaseModel):
    """Response of ``GET /pc/v6/jobs``. An empty search omits ``ergebnisliste``."""

    total: int = Field(validation_alias="maxErgebnisse")
    page: int = Field(validation_alias="page")
    size: int = Field(validation_alias="size")
    jobs: list[JobSummary] = Field(
        default_factory=list, validation_alias="ergebnisliste"
    )


class JobDetails(JobBase):
    """Response of ``GET /pc/v4/jobdetails/{base64(refnr)}``."""

    description: str | None = Field(
        default=None, validation_alias="stellenangebotsBeschreibung"
    )
    is_temp_agency: bool | None = Field(
        default=None, validation_alias="istArbeitnehmerUeberlassung"
    )
    is_private_placement: bool | None = Field(
        default=None, validation_alias="istPrivateArbeitsvermittlung"
    )
    partner_name: str | None = Field(
        default=None, validation_alias="allianzpartnerName"
    )
    partner_url: str | None = Field(default=None, validation_alias="allianzpartnerUrl")
