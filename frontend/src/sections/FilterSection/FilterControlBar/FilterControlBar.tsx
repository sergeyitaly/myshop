import { useTranslation } from "react-i18next"
import { TextButton } from "../../../components/UI/TextButton/TextButton"
import { useToggler } from "../../../hooks/useToggler"
import { SortMenuItem, useSortList } from "../SortList"
import { SortMenu } from "../SortMenu/SortMenu"
import styles from './FilterControlBar.module.scss'

interface FilterControlBarProps  {
    isOpenFilterMenu: boolean
    changeOrdering?: (orderName: string) => void
    onClickOpenFilterMenu: () => void
}

export const FilterControlBar = ({
    isOpenFilterMenu,
    changeOrdering,
    onClickOpenFilterMenu,

}: FilterControlBarProps) => {


    const sortList = useSortList()

    const { t } = useTranslation();


    const {
        openStatus: openSort,
        handleClose: closeSortMenu,   
        handleOpen: handleClickSort
    } = useToggler();

 

    const handleClickSortMenu = (item: SortMenuItem ) => {
        changeOrdering && changeOrdering(item.name)
        closeSortMenu()
    }

    

    
    
    return (
        <div  className={styles.bar} >
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