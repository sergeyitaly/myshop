import { useTranslation } from "react-i18next"
import { TextButton } from "../../../components/UI/TextButton/TextButton"
import { useToggler } from "../../../hooks/useToggler"
import { SortMenuItem, useSortList } from "../SortList"
import { SortMenu } from "../SortMenu/SortMenu"
import styles from './FilterControlBar.module.scss'
import { useEffect, useRef } from "react"

interface FilterControlBarProps  {
    isOpenFilterMenu: boolean
    changeOrdering?: (orderName: string) => void
    onClickOpenFilterMenu: () => void
    onInitRect: (rect?: DOMRect) => void
}

export const FilterControlBar = ({
    isOpenFilterMenu,
    changeOrdering,
    onClickOpenFilterMenu,
    onInitRect

}: FilterControlBarProps) => {

    const ref = useRef<HTMLDivElement>(null)

    const sortList = useSortList()

    const { t } = useTranslation();

    const rect = ref.current?.getBoundingClientRect()

    const {
        openStatus: openSort,
        handleClose: closeSortMenu,   
        handleOpen: handleClickSort
    } = useToggler();

    useEffect(() => {
        onInitRect(rect)
    }, [rect?.top])

 

    const handleClickSortMenu = (item: SortMenuItem ) => {
        changeOrdering && changeOrdering(item.name)
        closeSortMenu()
    }

    

    
    
    return (
        <div ref = {ref} className={styles.bar} >
            {
                isOpenFilterMenu ?
                    <span />
                    :
                    <TextButton
                        title={isOpenFilterMenu ? t('filters.hide') : t('filters.show')}
                        onClick={onClickOpenFilterMenu}
                    />
            }
            <TextButton
                title={t('sort.title')}
                onClick={handleClickSort}
            />
            {
                openSort &&
                <SortMenu
                    className={styles.sortMenu}
                    menuList={sortList}
                    onClickOutside={closeSortMenu}
                    onClickMenu={handleClickSortMenu}
                />
            }
        </div>
    )
}