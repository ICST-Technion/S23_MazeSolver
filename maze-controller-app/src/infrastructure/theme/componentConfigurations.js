export const carouselSizes = {
  photoHeightDefaultSize: 250,
};

export const detailedApartmentViewSizes = {
  imageHeight: 350,
  wordsInDescriptionSummary: 500,
};

export const apartmentInfoCard = {
  imageHeight: 250,
};

export const profileSizes = {
  profileSummaryPhotoSize: 64,
};

export const showingsSizes = {
  calendarIconSize: 32,
};

export const apartmentDetailsConf = {
  numDetailsInSummary: 5,
  detailToName: {
    neighbourhood: "neighbourhood",
    containsDishwasher: "Dishwasher",
    containsAirConditioning: "Air Conditioning",
    containsDryer: "Dryer",
    containsLaundryMachine: "Laundry Machine",
    containsBunker: "Bunker",
    isFurnished: "Furnished",
    petsAllowed: "Pets Allowed",
    hasPets: "Contains Pets",
    petType: "Pet Type",
    containsElevator: "Elevator",
    containsParking: "Parking",
    wifiInstalled: "Wifi Installed",
    numberOfRooms: "Number of Rooms",
    privateBathroom: "Bathroom In Room",
    floor: "floor",
  },
  detailIcons: {
    neighbourhood: "home-city-outline",
    Dishwasher: "dishwasher",
    "Air Conditioning": "snowflake",
    Dryer: "tumble-dryer",
    "Laundry Machine": "washing-machine",
    Bunker: "shield",
    Furnished: "table-furniture",
    "Pets Allowed": "dog",
    "Contains Pets": "dog",
    "Pet Type": "dog",
    Elevator: "elevator",
    Parking: "parking",
    "Wifi Installed": "wifi",
    "Number of Rooms": "door",
    "Bathroom In Room": "toilet",
    floor: "stairs",
  },
  isDetailBool: {
    neighbourhood: 0,
    Dishwasher: 1,
    "Air Conditioning": 1,
    Dryer: 1,
    "Laundry Machine": 1,
    Bunker: 1,
    Furnished: 1,
    "Pets Allowed": 1,
    "Contains Pets": 1,
    "Pet Type": 0,
    Elevator: 1,
    Parking: 1,
    "Wifi Installed": 1,
    "Number of Rooms": 0,
    "Bathroom In Room": 1,
    floor: 0,
  },
};

export const apartmentFiltersConf = {
  booleanFilters: [
    "containsDishwasher",
    "containsAirConditioning",
    "containsDryer",
    "containsLaundryMachine",
    "containsBunker",
    "isFurnished",
    "petsAllowed",
    "containsElevator",
    "containsParking",
    "wifiInstalled",
    "privateBathroom",
  ],
  sliderFilters: ["price"],
  singleSelectFilters: ["neighbourhood", "numberOfRooms", "floor"],
  checkboxSize: 24,
  sliderPassedColor: "lightgreen",
  sliderAheadColor: "dimgray",
  filterButtonColors: "lightblue",
};
