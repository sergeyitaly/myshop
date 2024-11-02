import { Skeleton } from "../../Skeleton/Skeleton"
import style from './ValueBox.module.scss'


export const ValueBoxSkeleton = () => {
    return (
        <Skeleton
            className={style.box}
        />
    )
}