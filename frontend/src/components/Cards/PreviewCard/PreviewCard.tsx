import clsx from 'clsx'
import { AppImage } from '../../AppImage/AppImage'
import style from './PreviewCard.module.scss'
import { Currency } from '../../../models/entities'
import { formatPrice } from '../../../functions/formatPrice'
import { Plug } from '../../Plug/Plug'
import { countDiscountPrice } from '../../../functions/countDiscountPrice'


interface PreviewCardProps {
    className?: string
    photoSrc: string | null
    previewSrc: string | null
    discount?: string
    currency?: Currency
    price?: string
    title: string
    subTitle?: string 
    loading?: boolean
    onClick?: () => void  
}


export const PreviewCard = ({
    className,
    photoSrc,
    title,
    discount,
    previewSrc,
    price,
    loading,
    currency,
    subTitle,
    onClick
}: PreviewCardProps) => {

    const handleClick = () => {
        onClick && onClick()
    }

   const discountPrice = countDiscountPrice(price, discount)
    

    return (
        <div 
            className={clsx(style.card, className, {
                [style.loading] : loading
            })}
            onClick={handleClick}
        >
              <AppImage
                className={style.imageSize}
                src={photoSrc}
                previewSrc={previewSrc}
                alt={title}
              />
            <p className={style.title}>{title}</p>
            {subTitle && <p className={style.subTitle}>{subTitle}</p>}
            {
                price && currency &&
                <div className={style.priceContainer}>
                    <p 
                        className={clsx(style.subTitle, {[style.crossText]: !!discountPrice} )}
                    >
                        {formatPrice(price, currency)}
                    </p>
                    {discountPrice && 
                        <p 
                            className={clsx(style.subTitle, style.currentPrice)}
                        >
                            {formatPrice(discountPrice, currency)}
                        </p>}
                </div>
            }
            {
                discountPrice &&
                <Plug
                    className={style.plug}
                />
            }
        </div>
    )
}