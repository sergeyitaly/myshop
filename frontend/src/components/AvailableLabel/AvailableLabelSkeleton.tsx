import { Skeleton } from "../Skeleton/Skeleton"
import style from './AvailableLable.module.scss'


export const AvailableLabelSkeleton = () => {
    return (
        <Skeleton
            className={style.skeleton}
        />
    )
}