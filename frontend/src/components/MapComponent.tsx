import { Fragment } from "react"

interface MapComponentProps {
    component: JSX.Element,
    qty: number
}

export const MapComponent = ({
    component,
    qty
}: MapComponentProps) => {

    const array = Array.from({length: qty}, (v, i) => i);

    return (
        <> 
            { array.map((number) => (
                <Fragment key={number}>
                    {component}
                </Fragment>
            )
            ) }
        </>
    ) 
}