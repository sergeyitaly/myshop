import { useEffect, useState } from 'react'
import { Product, ProductVariantsModel } from '../../models/entities'
import { PageContainer } from '../containers/PageContainer'
import { DropDown } from './components/DropDown/DropDown'
import { ProductControl } from './components/ProductControl/ProductControl'
import { Modal, useMediaQuery } from '@mui/material'
import style from './ProductInfoSection.module.scss'
import { screens } from '../../constants'
import { ProductImageSlider } from './components/ProductImageSlider/ProductImageSlider'
import { ProductImageSlide } from './components/ProductImageSlide/ProductImageSlide'



interface ProductInfoSectionProps {
    product: Product
    productVariants: ProductVariantsModel
    onChangeColor?: (color: string) => void
    onChangeSize?: (size: string) => void
}

export const ProductInfoSection = ({
    product,
    productVariants,
    onChangeColor,
    onChangeSize
}: ProductInfoSectionProps) => {

    
    const [currentImage, setCurrentImage] = useState<string | null>(product.photo)
    const [bigImage, setBigImage] = useState<string | null>(null)

    const isMobile = useMediaQuery(screens.maxMobile)


    useEffect(() => {
        setCurrentImage(product.photo)
    }, [product.photo])
  

    const openModal = () => {
        setBigImage(currentImage)
    }

    const closeModal = () => {
        setBigImage(null)
    }

    return (
    <>
        <section >
            <PageContainer className={style.container}>
                {
                    isMobile ?
                    <ProductImageSlider
                        className={style.imageBox}
                        images={product.images}
                        onClickZoom={openModal}
                     />
                    :
                    <>
                        <div className={style.wrapper}>
                            <div className={style.imageList}>
                                {
                                    product.images?.map((image) => (
                                    <div 
                                        key={image.id}
                                        className={style.previevBox}
                                        onClick={() => setCurrentImage(image.images)}
                                    >
                                        <img src={image.images}/>
                                    </div>
                                    ))
                                }
                            </div>
                        </div>
                        {
                        currentImage &&
                        <ProductImageSlide
                            className={style.imageBox}
                            src={currentImage}
                            alt={product.name}
                            onClickZoom={openModal}
                        />
                        }
                    </>
                }
            
                <div className={style.productInfo}>
                    <ProductControl 
                        product={product}
                        variants={productVariants}
                        onChangeColor={onChangeColor}
                        onChangeSize={onChangeSize}
                    />
                    <div className={style.description}>
                        <h3>Опис:</h3>
                        <p>{product.description ? product.description : 'опис товару поки що відсутній'}</p>
                    </div>
                </div>

                <DropDown
                    className={style.applyDropdown}
                    changebleParam={product.id}
                    title='Застосування:'
                    content={product.usage || ''}
                />
                <DropDown
                    className={style.careDropdown}
                    changebleParam={product.id}
                    title='Догляд:'
                    content={product.maintenance || ''}
                />
            </PageContainer>
        </section>
        <Modal
            open={!!bigImage}
            className={style.center}
        >
            {
                bigImage ?
                <div 
                    className={style.zoomImage}
                    onClick={closeModal}
                >
                    <img src={bigImage} />
                </div>
                :
                <div>No image</div>
            }
        </Modal>
    </>
    )
}