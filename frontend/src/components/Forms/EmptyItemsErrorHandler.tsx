import { useField, useFormikContext } from "formik"
import { useSnackbar } from "../../hooks/useSnackbar"
import { useEffect } from "react"

interface EmptyItemsErrorHandlerProps{
    name: string
}

export const EmptyItemsErrorHandler = ({
    name
}: EmptyItemsErrorHandlerProps) => {

    const [_, meta] = useField(name)

    const {isSubmitting} = useFormikContext()

    const {openInfo} = useSnackbar()

    useEffect(() => {
        isSubmitting && meta.error &&
        openInfo(meta.error, 'warning')

    }, [meta.error, isSubmitting, openInfo])
    
    return null
}