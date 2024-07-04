import { DetailedHTMLProps, HTMLAttributes } from "react"
import clsx from "clsx"
import style from './Skeleton.module.scss'

interface SkeletonProps extends DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    
}

export const Skeleton = ({
    ...props
}: SkeletonProps) => {

    const { className } = props

    


    return (
        <div {...props} className={clsx(className, style.box)} />
    )
}