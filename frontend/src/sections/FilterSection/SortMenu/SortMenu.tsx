import clsx from 'clsx'
import styles from './SortMenu.module.scss'
import { DetailedHTMLProps, HTMLAttributes, useRef } from 'react'
import useClickOutside from '../../../hooks/useClickOutside'
import { SortMenuItem } from '../SortList'



interface SortMenuProps extends  DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement> {
    menuList?: SortMenuItem[]
    onClickOutside: () => void
    onClickMenu: (sortBy: SortMenuItem) => void
}


export const SortMenu = ({
    menuList = [],
    onClickOutside,
    onClickMenu,
    ...props
}: SortMenuProps) => {


    const sortRef = useRef<HTMLDivElement>(null)

    useClickOutside(sortRef, onClickOutside) 


    return (
        <div 
            ref={sortRef}
            className={clsx(props.className, styles.container)}

        >
            {
                menuList.map((item) => {

                    const {title, name} = item

                    return (
                        <button 
                            key = {name}
                            className={styles.button}
                            onClick={() => onClickMenu(item)}
                        >
                            {title}
                        </button>
                    )
                })
            }
        </div>
    )
}