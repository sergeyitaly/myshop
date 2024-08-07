import { useState } from "react"


export const useCounter = (initialQty: number) => {

    const [qty, setQty] = useState<number>(initialQty)

    const handleIncrement = () => {
        setQty((prevQuantity) => prevQuantity + 1);
      };
    
    const handleDecrement = () => {
      if (qty > 1) {
        setQty((prevQuantity) => prevQuantity - 1);
      }
    };

    const setCounter = (number: number) => {
      setQty(number)
    }

    return {
        qty,
        handleIncrement,
        handleDecrement,
        setCounter
    }
}