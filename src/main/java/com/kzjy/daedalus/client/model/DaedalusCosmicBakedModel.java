package com.kzjy.daedalus.client.model;

import net.minecraft.client.resources.model.BakedModel;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.neoforge.client.model.BakedModelWrapper;

import java.util.List;

/**
 * 临时简化版：前置渲染库（RenderBlenderLib）移植期间不执行任何特效渲染，
 * 仅作为一个 BakedModel 包装器透传，保证 DaedalusModelLoader 可以正常编译。
 * 前置库就绪后，用 git 恢复 .rb.bak 或重新应用原实现即可。
 */
public class DaedalusCosmicBakedModel extends BakedModelWrapper<BakedModel> {

    @SuppressWarnings("unused")
    private final List<ResourceLocation> maskSprite;
    @SuppressWarnings("unused")
    private final int glowColor;
    @SuppressWarnings("unused")
    private final float glowWidth;
    @SuppressWarnings("unused")
    private final float glowOffset;
    @SuppressWarnings("unused")
    private final boolean isNeo;
    @SuppressWarnings("unused")
    private final int neoType;

    public DaedalusCosmicBakedModel(BakedModel wrapped,
                                    List<ResourceLocation> maskSprite,
                                    int glowColor, float glowWidth, float glowOffset,
                                    boolean isNeo, int neoType) {
        super(wrapped);
        this.maskSprite = maskSprite;
        this.glowColor = glowColor;
        this.glowWidth = glowWidth;
        this.glowOffset = glowOffset;
        this.isNeo = isNeo;
        this.neoType = neoType;
    }

    public DaedalusCosmicBakedModel(BakedModel wrapped, List<ResourceLocation> maskSprite) {
        this(wrapped, maskSprite, 0, 0, 0, false, 0);
    }
}
