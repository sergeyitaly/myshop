import { useRef } from "react";
import { useTranslation } from "react-i18next";
import { useToggler } from "../../../hooks/useToggler";
import { AppIconNames } from "../../../constants";
import { LanguageButton } from "../LanguageButton/LanguageButton";
import useClickOutside from "../../../hooks/useClickOutside";
import styles from './LanguageDropDown.module.scss'
import { AppIcon } from "../../../components/SvgIconComponents/AppIcon";
import clsx from "clsx";

export interface Language {
    icon: AppIconNames
    title: string
    lang: 'uk' | 'en'
}

const languages: Language[] = [
    {
        icon: 'flagUkraine',
        title: 'Українська',
        lang: 'uk'
    },
    {
        icon: 'flagUK',
        title: 'English',
        lang: 'en'
    }
]


export const LanguageDropDown = () => {

    const { i18n } = useTranslation();

    const {openStatus, handleToggle, handleClose} = useToggler()

    const menuList = useRef<HTMLDivElement>(null)

    useClickOutside(menuList, handleClose)


    const handleLanguageChange = (lang: string) => {
        i18n.changeLanguage(lang); // Change the language
        handleClose()
    };

    const getLanguage = (inpLang: string) => {
        return languages.find(({lang}) => inpLang === lang ) as Language 
    } 

    return (
        <div className={styles.menuContainer}>
            <div
                className={styles.dropDownButton}
                onClick={handleToggle}
            >
                <LanguageButton 
                    className={styles.button}
                    language={getLanguage(i18n.language)}
                />
                <AppIcon className={clsx(styles.arrow, {[styles.active]: openStatus})} iconName="forwardArrow"/>
            </div>
            {
              openStatus &&  
                <div 
                    ref = {menuList}
                    className={styles.menuList}
                >
                   {
                    languages.map((language) => (
                        <LanguageButton
                            key={language.lang}
                            language={language}
                            onClick={handleLanguageChange}
                        />
                    ))
                   }
                </div>
            }
        </div>
    )
}