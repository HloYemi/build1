package com.kzjy.daedalus.client.gui;

import net.minecraft.network.chat.Component;
import net.minecraft.world.inventory.tooltip.TooltipComponent;

/**
 * @author Kzjy<br>
 * 奇迹附魔 Tooltip 数据载体<br>
 * 用于在服务端/逻辑端传递 Tooltip 信息至客户端渲染器
 */
public record MiracleTooltipData(Component text) implements TooltipComponent {
}
