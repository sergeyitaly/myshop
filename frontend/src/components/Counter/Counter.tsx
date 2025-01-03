import { useEffect, useState } from "react";
import clsx from "clsx";
import style from "./Counter.module.scss";

interface CounterProps {
	value: number;
	stock: number;
	className?: string;
	onChangeCounter?: (number: number) => void;
}

export const Counter = ({
	value,
	stock,
	className,
	onChangeCounter,
}: CounterProps) => {
	const [val, setVal] = useState<number>(value);

	useEffect(() => {
		onChangeCounter && onChangeCounter(val);
	}, [val]);

	useEffect(() => {
		setVal(value);
	}, [value]);

	const handleReduce = () => {
		if (val > 1) {
			setVal(val - 1);
			onChangeCounter && onChangeCounter(val - 1);
		}
	};

	const handleIncrement = () => {
		if (val < stock) {
			setVal(val + 1);
			onChangeCounter && onChangeCounter(val + 1);
		}
	};

	return (
		<div className={clsx(style.container, className)}>
			<button onClick={handleReduce} disabled={stock === 0}>-</button>
			<input type="number" value={val} readOnly />
			<button onClick={handleIncrement} disabled={stock === 0}>+</button>
		</div>
	);
};
