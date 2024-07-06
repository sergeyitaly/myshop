import { TextField } from "@mui/material"
import { useField, useFormikContext } from "formik"
import { DetailedHTMLProps, InputHTMLAttributes, useEffect, useState } from "react"

interface FormikInputProps extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> {
    label: string
    name: string
}


export const FormikInput = ({
    label,
    ...props
}: FormikInputProps) => {

    const [field, meta] = useField(props)

    const {error, touched} = meta

        const {isSubmitting} = useFormikContext()

        const [clicked, setClicked] = useState<boolean>(false)

        useEffect(() => {
            isSubmitting && setClicked(true)
        }, [isSubmitting])

        useEffect(() => {
            setClicked(false)
        }, [field.value])
        

    return (
        <TextField 
            fullWidth
            label={label} variant="outlined"
            {...field}
            error = {clicked && !!error && !!touched}
            helperText = {clicked && !!error && !!touched && error}
        />
    )
}