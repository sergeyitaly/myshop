import { TransformComponent, TransformWrapper } from "react-zoom-pan-pinch"
import image from '../assets/Woman in computer giving heart-shaped present to man.png'



export const TestPage = () => {

   return (
    <div>
         <TransformWrapper>
            <TransformComponent>
                  <img 
                     src={image}
                  />
            </TransformComponent>
         </TransformWrapper>
    </div>
   )
}