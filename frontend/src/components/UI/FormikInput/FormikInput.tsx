import { TextField } from "@mui/material"
import { useField } from "formik"
import { DetailedHTMLProps, InputHTMLAttributes } from "react"

interface FormikInputProps extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> {
    label: string
    name: string
}


export const FormikInput = ({
    label,
    ...props
}: FormikInputProps) => {

    const [field] = useField(props)

    return (
        <TextField 
            fullWidth
            label={label} variant="outlined"
            {...field}
        />
    )
}