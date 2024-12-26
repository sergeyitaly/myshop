import { useField } from "formik";

interface FormikRadioButtonProps {
	className?: string;
	name: string;
	value: string;
	label: string;
}

export const FormikRadioButton = ({
	className,
	value,
	label,
	...props
}: FormikRadioButtonProps) => {
	const [field] = useField({ ...props, type: "radio", value });

	return (
		<label className={className}>
			<input type="radio" {...field} value={value} />
			<span>{label}</span>
		</label>
	);
};
