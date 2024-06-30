from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator
from app.models import ImageToTextHistory
from llm_model import PROMPT_TYPE_MAP, LLM_MODEL_MAP
import llm_model
from predict_model import MODEL_PREDICT_DICT
from PIL import Image
import io
import copy

# Create your views here.


def index(request):
    images_list = ImageToTextHistory.objects.all().order_by("-id")
    paginator = Paginator(images_list, 25)  # 每页显示25个图像
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    # 计算页码范围
    current_page = page_obj.number
    total_pages = paginator.num_pages
    max_pages_to_show = 5

    start_page = max(current_page - max_pages_to_show // 2, 1)
    end_page = start_page + max_pages_to_show - 1

    if end_page > total_pages:
        end_page = total_pages
        start_page = max(end_page - max_pages_to_show + 1, 1)

    page_range = range(start_page, end_page + 1)

    return render(
        request,
        "index.html",
        {
            "page_obj": page_obj,
            "page_range": page_range,
        },
    )


@csrf_exempt
def upload_view(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        img_to_text_model = request.POST.get("img_to_text_model")
        llm_type = request.POST.get("llm_type")
        model_name = request.POST.get("model_name")
        prompt_type = request.POST.get("prompt_type")
        try:
            # 这里需要把图片分两步处理，需要先用LLM模型生成prompt，然后用img_to_text_model模型生成text
            # 图生文需要传入Image.Image对象
            prompt_func = PROMPT_TYPE_MAP.get(prompt_type)
            ll_model_obj = LLM_MODEL_MAP.get(llm_type)
            llm_model_instance = getattr(llm_model, ll_model_obj.get("LLMCLass"))
            predict_model_instance = MODEL_PREDICT_DICT.get(img_to_text_model)
            image_image = Image.open(io.BytesIO(image.read()))

            input_sentence = predict_model_instance().predict(image_image)

            prompt = prompt_func(input_sentence)
            text = llm_model_instance(model_name=model_name).generate(prompt)
        except Exception as e:
            import traceback

            print(traceback.format_exc())

            return JsonResponse({"error": str(e)}, status=500)
        new_image = copy.deepcopy(image)
        # 保存预测历史
        img = ImageToTextHistory.objects.create(
            image=new_image,
            text=text,
            image_text=input_sentence,
            llm_model=llm_type,
            model_name=model_name,
        )
        image_src = img.image.url
        return JsonResponse(
            {"image_src": image_src, "text": text, "image_text": input_sentence}
        )
    else:
        content = {
            "MODEL_PREDICT_DICT": MODEL_PREDICT_DICT,
            "PROMPT_TYPE_MAP": PROMPT_TYPE_MAP,
            "LLM_MODEL_MAP": LLM_MODEL_MAP,
        }
        return render(request, "upload.html", content)
