import image1 from "../../assets/collection/Rectangle 48.svg";
import image2 from "../../assets/collection/Rectangle 69.svg";
import image3 from "../../assets/collection/Rectangle 70.svg";
import image4 from "../../assets/collection/Rectangle 71.svg";
import image5 from "../../assets/collection/Rectangle 135.svg";
import image6 from "../../assets/collection/Rectangle 135 (1).svg";
import image7 from "../../assets/collection/Rectangle 135 (2).svg";
import image8 from "../../assets/collection/Rectangle 135 (3).svg";

interface Product {
  name: string;
  price: string;
  imageUrl: string;
  newPrice?: string;
  category?: string;
}

export const mockDataCollection: Product[] = [
  {
    name: "Каблучка Queen",
    price: "7 300,00 грн",
    imageUrl: image1,
  },
  {
    name: "Браслет Queen",
    price: "8 300,00 грн",
    imageUrl: image2,
  },
  {
    name: "Сет з каблучок",
    price: "10 300,00 грн",
    imageUrl: image3,
  },
  {
    name: "Сережки з цитрином",
    price: "5 600,00 грн",
    imageUrl: image4,
  },
  {
    name: "Каблучка Queen",
    price: "7 300,00 грн",
    imageUrl: image5,
  },
  {
    name: "Браслет Queen",
    price: "8 300,00 грн",
    imageUrl: image6,
  },
  {
    name: "Сет з каблучок",
    price: "10 300,00 грн",
    imageUrl: image7,
  },
  {
    name: "Сережки з цитрином",
    price: "5 600,00 грн",
    imageUrl: image8,
  },
];
