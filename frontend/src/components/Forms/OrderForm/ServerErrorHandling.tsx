import { useFormikContext } from "formik"
import { useEffect } from "react"

interface ServerErrorHandlingProps {
    errors: {
        name?: string
        surname?: string
        phone?: string
        email?: string
        receiver?: string
        receiver_comments?: string
        order_items?: string
    } | null
}

export const ServerErrorHandling = ({
    errors
}: ServerErrorHandlingProps) => {

    const {setErrors} = useFormikContext()

    useEffect(() => {
        errors &&
        setErrors(errors)
    }, [errors])

    return (<></>)
}