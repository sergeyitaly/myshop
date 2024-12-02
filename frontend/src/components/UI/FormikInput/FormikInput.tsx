 import { useField, useFormikContext } from "formik"
import { ChangeEvent, DetailedHTMLProps, InputHTMLAttributes, useEffect, useState } from "react"
import { AppInput } from "../AppInput/AppInput"
import { formatPhoneNumber } from "../../../functions/phoneFormatter"

interface FormikInputProps extends DetailedHTMLProps<InputHTMLAttributes<HTMLInputElement>, HTMLInputElement> {
    label: string
    name: string
}


export const FormikInput = ({
    label,
    ...props
}: FormikInputProps) => {

    const [field, meta, helpers] = useField(props)

    const {error, touched} = meta

        const {isSubmitting} = useFormikContext()

        const [clicked, setClicked] = useState<boolean>(false)

        useEffect(() => {
            isSubmitting && setClicked(true)
        }, [isSubmitting])

        useEffect(() => {
            setClicked(false)
        }, [field.value])
        
        

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
            if(field.name === 'phone'){
                helpers.setValue(formatPhoneNumber(e.target.value).phone)
                return
            }
            field.onChange(e)
    }

    return (
        <AppInput 
            label={label}
            {...field}
            value={field.name === 'phone' ? formatPhoneNumber(field.value).formatedPhone : field.value}
            onChange={handleChange}
            {...props}
            error = {clicked && !!error && !!touched}
            helperText = {error}
        />
    )
}